#! python

import argparse
from Bio import AlignIO

parser=argparse.ArgumentParser(description='This program converts fasta to phylip')
parser.add_argument('-i','--input',dest='inp',required=True,help='Input fasta file')
parser.add_argument('-o','--output',dest='out',required=False,default='converted.phy',help='Output file of converted sequences [Default: converted.phy]')
args=parser.parse_args()

outfile=open(args.out,'w')
for rec in AlignIO.parse(args.inp,'fasta'):
    AlignIO.write(rec,outfile,'phylip')
outfile.close()
