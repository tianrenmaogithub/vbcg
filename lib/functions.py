import os
import sys
import subprocess as subp
from multiprocessing import Pool
from glob import glob
from io import StringIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import SeqIO
import pandas as pd
import re
home = os.path.dirname(os.path.realpath(__file__))

def call(cmd='',out='',err='',ex=True):
    if subp.call('set -ex; '+cmd,shell=True)==0:
        print(out)
    else:
        if ex:
            print(err)
            sys.exit(1)
        else:
            return()

# prodigal gene prediction
def prodigal(infile, outdir):
    print('Prodigal for %s' % os.path.basename(infile))
    call('prodigal -a %s/%s.faa -o %s/prodigal.out -i %s -p meta -q' % (outdir, os.path.basename(infile), outdir, infile), 'Prodigal prediction for %s completed.' % infile, 'Prodigal prediction for %s failed.' % infile)

def run_prodigal(indir, outdir, nproc=10):
    print('--------------- Running Prodigal gene prediction for %s -----------------' % indir)
    os.system('gzip -d %s/*.gz' % indir)
    os.system('rm -rf %s; mkdir %s' % (outdir, outdir))

    pool = Pool(nproc)
    for i in os.listdir(indir):
        pool.apply_async(prodigal, ('%s/%s' % (indir, i), outdir,))

    pool.close()
    pool.join()

# hmmscan gene annotation
def hmmscan(infile, outfile1, outfile2, profile):
    call('hmmscan -o '+outfile1+' --tblout '+outfile2+' --noali --cut_tc --cpu 1 '+profile+' '+infile, out=infile+' hmmscan finished', err=infile+' hmmscan failed')

def run_hmmscan(prodigal_outdir, outdir, profile, nproc=10):
    print('--------------- Running hmmscan for %s --------------- ' % prodigal_outdir)
    os.system('rm -rf %s; mkdir %s' % (outdir, outdir))
    
    pool = Pool(nproc)
    for i in glob('%s/*faa' % prodigal_outdir):
        pool.apply_async(hmmscan, (i, '%s/%s.out' % (outdir, os.path.basename(i)), '%s/%s.tbl' % (outdir, os.path.basename(i)), profile,))
    
    pool.close()
    pool.join()

# retrieve vbcg genes
def parse_hmm_out(hmm_out):
    '''
    output: protein ID - hmm ID
    '''
    hmm = open(hmm_out, 'r').readlines()
    hmm = [i[:100] for i in hmm]
    hmm = '-\n'.join(hmm)
    df1 = pd.read_csv(StringIO(hmm), sep=' +', header=None, index_col=None, comment='#', engine='python')
    df1.dropna(inplace=True)
    df2  = df1.loc[:,[1,2]]
    df2.drop_duplicates(1, inplace=True)
    dict1 = df2.set_index(1).to_dict()[2]

    return(dict1)

def retrieve_vbcg(hmmscan_outdir, prodigal_outdir, vbcg_outdir):
    print('--------------- Retrieving vbcg genes from prodigal output based on hmmscan output--------------- ')
    os.system('rm -rf %s; mkdir %s' % (vbcg_outdir, vbcg_outdir))

    faa = [os.path.basename(i) for i in glob('%s/*.faa' % prodigal_outdir)]
    d = {i: parse_hmm_out('%s/%s.tbl' % (hmmscan_outdir, i)) for i in faa}
    df = pd.DataFrame.from_dict(d)
    
    df2 = df.copy()
    for i in df.columns:
        d = SeqIO.to_dict(SeqIO.parse('%s/%s' % (prodigal_outdir, i), 'fasta'))
        for j in df.index:
            if df.isnull().loc[j,i]:
                continue
            rec = d[df.loc[j,i]]
            rec.id = '%s_%s' % (i, rec.id)
            df2.loc[j,i] = rec

    for i in df2.index:
        SeqIO.write([j for j in df2.loc[i,:] if type(j)!=float], '%s/%s.faa' % (vbcg_outdir, i), 'fasta')

    print('Retrieving VBCG genes done')

# align, trim, concatenate and make tree
def concatenate_genes(infiles, outdir):
    dict1 = {}
    for i in infiles:
        dict1[i] = SeqIO.to_dict(SeqIO.parse(i, 'fasta'))

    df = pd.DataFrame.from_dict(dict1)
    df.dropna(axis=0, inplace=True)

    recs = []
    for i in df.index:
        rec = SeqRecord(id=i, seq=Seq(''.join([str(j.seq) for j in df.loc[i,:]])))
        recs.append(rec)

    outfile = 'concat_%s_taxa.fas' % df.shape[0]
    SeqIO.write(recs, '%s/%s' % (outdir, outfile), 'fasta')

    return(outfile)

def make_tree(dir1, tree_maker, cpu, dir2):
    print('--------------- Align, trim, concatenate and make tree--------------- ')
    os.chdir(dir1)
    for i in glob('*.faa'):
        gene = i.replace('.faa', '')
        call('%s/../bin/muscle -in %s -out %s.aln 2> %s/error.log' % (home, i, gene, dir2), '%s alignment done' % i, '%s alignment failed. Please check the version of your muscle.' % i)
        call('python %s/../bin/trim_terminal_gaps_from_alignment.py -i %s.aln -o %s.aln.trimmed' % (home, gene, gene), '%s alignment trimming done' % i, '%s alignment trimming failed' % i)

    l = sum([[rec.id for rec in SeqIO.parse(i, 'fasta')] for i in glob('*.faa')], [])
    l = set([i.split('.faa_')[0] for i in l])
    d = dict(zip(l, ['taxon%s' % i for i in range(len(l))]))
    d2 = dict(zip(['taxon%s' % i for i in range(len(l))], l))

    for i in glob('*.aln.trimmed'):
        recs = list(SeqIO.parse(i, 'fasta'))
        for rec in recs:
            rec.id = str(d[rec.id.split('.faa_')[0]])
            rec.description = ''
        SeqIO.write(recs, i+'.renamed', 'fasta')

        call('%s/../bin/gblocks %s.renamed -t=\'p\' -b4=3 -b5=h' % (home, i), '%s GBlocks done' % i, '%s GBlocks failed' % i, ex=False)
    os.system('rm -rf *htm')
    
    con = concatenate_genes(glob('*-gb'), '.')
    call('python %s/../bin/fasta2phylip.py -i %s -o %s' % (home, con, con.replace('.fas', '.phy')), 'Phylip converted', 'Phylip convert failed')

    if tree_maker == 'fasttree':
        call('%s/../bin/fasttree -out %s -lg -gamma %s' % (home, con.replace('.fas', '.nwk'), con.replace('.fas', '.phy')), 'FastTree done', 'FastTree failed')
    elif tree_maker == 'raxml':
        call('%s/../bin/raxml -f a -k -s %s -m PROTGAMMALG -n %s -x 12345 -p 12345 -N 100 -T %s' % (home, con.replace('.fas', '.phy'), os.path.basename(con.replace('.fas', '.nwk')), cpu), 'RAxML done', 'RAxML failed')
        os.rename('RAxML_bipartitionsBranchLabels.%s' % con.replace('.fas', '.nwk'), con.replace('.fas', '.nwk'))
    else:
        print('Error: Unknown tree maker')
        sys.exit(1)

    nwk = open(con.replace('.fas', '.nwk'), 'r').read()
    nwk = re.sub(r'taxon\d+', lambda x: d2[x.group(0)], nwk)
    open('../concatenated_ML_tree.nwk', 'w').write(nwk)
    os.chdir(dir2)

