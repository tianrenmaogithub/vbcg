# VBCG: 20 validated bacterial core genes for phylogenomic analysis with high fidelity and resolution
### Background
Phylogenomic analysis has become an inseparable part of studies of bacterial diversity and evolution, and many different bacterial core genes have been collated and used for phylogenomic tree reconstruction. However, these genes have been selected based on their presence and single-copy ratio in all bacterial genomes, leaving out the gene's 'phylogenetic fidelity' unexamined. 
### Results
From 30,522 complete genomes covering 11,262 species, we examined 148 bacterial core genes that have been previously used for phylogenomic analysis. In addition to the gene presence and single-copy rations, we evaluated the gene's phylogenetic fidelity by comparing each gene's phylogeny with its corresponding 16S rRNA gene tree. Out of the 148 bacterial genes, 20 validated bacterial core genes (VBCG) were selected as the core gene set with the highest bacterial phylogenetic fidelity. Compared to the larger gene set, the 20-gene core set resulted in more species having all genes present and fewer species with missing data, thereby enhancing the accuracy of phylogenomic analysis. Using Escherichia coli strains as examples of prominent bacterial foodborne pathogens, we demonstrated that the 20 VBCG produced phylogenies with higher fidelity and resolution at species and strain levels while 16S rRNA gene tree alone could not. 
### Conclusion
The 20 validated core gene set improves the fidelity and speed of phylogenomic analysis. Among other uses, this tool improves our ability to explore the evolution, typing and tracking of bacterial strains, such as human pathogens. We have developed a Python pipeline and a desktop graphic app (available on GitHub) for users to perform phylogenomic analysis with high fidelity and resolution.
### Keywords
Phylogenomics; Bacterial core genes; Phylogenetic tree; Pathogen typing 

## Installation
### Linux
dependencies:<br>
- Bio >= 1.5.3<br>
- Pandas<br>
- Prodigal<br>
- HMMER<br>
To install the dependencies, run:<br>
conda create -n vbcg python=3.9<br>
pip install biopython pandas<br>
conda install -c bioconda prodigal hmmer<br>
Then download this package<br>
git clone https://github.com/tianrenmaogithub/vbcg.git<br>
and run this for the help message.<br>
python path_to_vbcg/bin/vbcg.py -h

### Windows
Download the <a href='https://hts.iit.edu/static/files/vbcg_v1.3_setup.exe'> <b> installer executable </b> </a> and install it to run the analysis in GUI mode. Click "More Info" and then "Run Anyway" to proceed with the installation.

<img src='gui.jpg' width=500px>

## Input data
You need to prepare a directory with separate genome sequence FASTA files (either zipped in .gz or not). Do not include any non-FASTA files or subfolders.

You may download this <a href='https://hts.iit.edu/static/files/example_input_genomes.zip'><b>example input genomes data</b></a> as a reference. Unzip it and feed the <b>directory</b> to the software as the input.

## Citation
If you found our tool helpful, please cite our paper.<br>
VBCG: 20 validated bacterial core genes for phylogenomic analysis with high fidelity and resolution<br>
https://www.biorxiv.org/content/10.1101/2023.06.13.544823v1
