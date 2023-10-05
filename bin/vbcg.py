#! python

import os
import argparse
home = os.path.dirname(os.path.realpath(__file__))
exec(open(home+'/../lib/functions.py', 'r').read())

parser=argparse.ArgumentParser(description='VBCG v1.3\nThis program build a phylogenomic tree of 20 validated bacterial core genes (VBCG) with input of whole genome sequence FASTA files. In addition, you can specify a custom bacterial core gene set with the option -H. \nThe processes include gene prediction with Prodigal, gene annotation with HMMER, protein sequence alignment with Muscle, alignment trimming with Gblock, ML tree reconstruction with FastTree or RAxML.\n',formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--indir', dest='indir', required=True, help='Input directory with whole genome sequence FASTA files')
parser.add_argument('-H', '--hmm', dest='hmm', required=False, default='%s/../lib/vbcg.hmm' % home, help='HMM models for core genes to concatenate. If you use a custom HMM model file, please index it using hmmpress first [Default: %s/../lib/vbcg.hmm]' % home)
parser.add_argument('-o', '--outdir', dest='outdir', required=False, default='vbcg_out', help='Output directory [Default: vbcg_out/]')
parser.add_argument('-m', '--tree_maker', dest='maker', required=False, default='fasttree', choices=['raxml','fasttree'],help='Tools for phylogenetic tree reconstruction. options include fasttree (FastTree) and raxml (RAxML). [Default: fasttree]')
parser.add_argument('-g','--genes', dest='missing_genes', required=False, type=int, default=4, help='Number of missing genes allowed for each species [default: 4]')
parser.add_argument('-n','--nproc', dest='nproc', required=False, type=int, default=10, help='Number of CPUs to use [default: 10]')

args=parser.parse_args()

# organize directories
os.system('rm -rf %s; mkdir %s' % (args.outdir, args.outdir))

# prodigal gene prediction
run_prodigal(args.indir, '%s/%s' % (args.outdir, 'prodigal'), args.nproc)

# hmmscan vbcg genes
run_hmmscan('%s/%s' % (args.outdir, 'prodigal'), '%s/%s' % (args.outdir, 'hmmscan'), args.hmm, nproc=args.nproc)

# retrieve vbcg genes
retrieve_vbcg('%s/%s' % (args.outdir, 'hmmscan'), '%s/%s' % (args.outdir, 'prodigal'), '%s/%s' % (args.outdir, 'vbcg_genes'))

# align, trim, concatenate, make tree
make_tree('%s/%s' % (args.outdir, 'vbcg_genes'), args.maker, args.nproc, os.getcwd(), args.missing_genes)
print('Done. See the output ML tree: %s/concatenated_ML_tree.nwk\nEnjoy it.' % args.outdir)

