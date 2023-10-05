# VBCG: 20 validated bacterial core genes for phylogenomic analysis with high fidelity and resolution
Phylogenomic analysis has become an inseparable part of studies of bacterial diversity and evolution, and many different bacterial core genes have been collated and used for phylogenomic tree reconstruction. However, these genes have been selected based on their presence and single-copy ratio in all bacterial genomes, leaving out the gene's 'phylogenetic fidelity' unexamined. From 30,522 complete genomes covering 11,262 species, we examined 148 bacterial core genes that have been previously used for phylogenomic analysis,. In addition to the gene presence and single-copy rations, we evaluated the gene's phylogenetic fidelity by comparing each gene’s phylogeny with its corresponding 16S rRNA gene tree. Out of the 148 bacterial genes, 20 validated bacterial core genes (VBCG) were selected as the core gene set with the highest bacterial phylogenetic fidelity. Moreover, the smaller gene set resulted in a higher species presence in the tree than larger gene sets. Using Escherichia and Salmonella as examples of prominent bacterial foodborne pathogens, we demonstrated that the 20 VBCG produced phylogenies with higher fidelity and resolution at species and strain levels while 16S rRNA gene tree alone could not. Among other uses, this tool improves our ability to investigate the origins of foodborne disease outbreaks. We have developed a Python pipeline and a desktop graphic app for users to perform phylogenomic analysis with high fidelity and resolution.
## Installation
### Linux / MacOS
dependencies:<br>
Bio >= 1.5.3<br>
Pandas<br>
Prodigal<br>
HMMER<br>

Download this package and run

python bin/vbcg.py -h for help message

### Windows
Download the <a href='https://hts.iit.edu/static/files/vbcg_v1.3_setup.exe'> <b> installer executable </b> </a> and install it to run the analysis in GUI mode. Click "More Info" and then "Run Anyway" to proceed with the installation.
<img src='gui.jpg' width=500px>

## Input data
You need to prepare a directory with separate genome sequence FASTA files (either zipped in .gz or not). 

## Citation
If you found our tool helpful, please cite our paper.<br>
VBCG: 20 validated bacterial core genes for phylogenomic analysis with high fidelity and resolution<br>
https://www.biorxiv.org/content/10.1101/2023.06.13.544823v1
