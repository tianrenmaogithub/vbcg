#! python

import argparse
from Bio import AlignIO,SeqIO
import re

parser=argparse.ArgumentParser(description='This program trims the terminal gaps of multiple alignments for further use like phylogenetic tree reconstructing.')
parser.add_argument('-i','--input',dest='inp',required=True,help='Input alignment fasta file')
parser.add_argument('-o','--output',dest='out',required=False,default='trimmed.fa',help='Output file of trimmed alignments [Default: trimmed.fa]')
args=parser.parse_args()

start=[]
end=[]

for rec in AlignIO.read(args.inp,'fasta'):
    search=re.search(r'^(-*).*?(-*)$',str(rec.seq))
    if search:
        start.append(len(search.group(1)))
        end.append(len(search.group(2)))

if start:
    s=max(start)
else:
    s=0


if end:
    e=max(end)
else:
    e=''

outfile=open(args.out,'w')
for rec in AlignIO.read(args.inp,'fasta'):
    if e:
        rec.seq=rec.seq[s:-e]
    else:
        rec.seq=rec.seq[s:]
    SeqIO.write(rec,outfile,'fasta')

outfile.close()

