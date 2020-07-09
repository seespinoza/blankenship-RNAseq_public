# blankenship-RNAseq
RNA-seq differential expression analyses on C. albicans.
*Note: count_data has been removed.

## Repository Directories
### DGE_R_scripts
R scripts used to run Differential Gene Expression analyses can be found here.

- *DESeq2.R*\
  Script that shows an example of how DESeq2 was run to calculate fold-change values.

- *edgeR.R*\
  Script that shows an example of how edgeR was run to calculate fold-change values.


### FC_tables
This directory contains all fold-change values in csv (comma seperated values) format.\
These files should be able to be opened in Excel and similar applications.\


- `30_min/`\
  All fold-change values for all 30 min experiments.
- `3_hr/`\
  All fold-change values for all 3 hr experiments.

**All fold change values were calculated using the YDP Liquid samples as the control group.**


### count_data
This directory contains text files with raw counts for every
RNA-seq experiment.

- *30_min_counts.txt*\
  Raw counts for the 30 minute data.

- *3_hr_counts.txt*\
  Raw counts for the 3 hr data.

- *countScripts/*\
  Directory with miscellaneous python scripts for data manipulation.

### pre_analysis_bash_scripts

The scripts in this directory were run in the following order:

1) *sra_dl.slurm*\
   Uses the SRA toolkit from NCBI to download all respective
   RNA-seq run files in .fastq format.

2) *generateIndices.slurm*\
   Genome indices are generated using the STAR read aligner.
   Indices are generated using genomic annotation and the full
   genome sequence (both in .gtf and .fna formats respectively).

3) *mapReads.slurm*\
   All of the RNA-seq reads are finally mapped to the reference
   genome with STAR using the indices created in the previous step.

4) *getRawCounts.slurm*\
   Using featureCounts, the raw counts of reads mapping to exons
   are obtained (Each gene in each sample has its own count).
   This step takes the .sam files created in the previous step as input.


**Warning** Both scripts 2 and 3 are memory and CPU intensive.
Make sure you have at least 32gb of RAM before running.

- *Note*: the scripts shown in this directory were used to analyze the 3
  hour data, but the same process should be followed to obtain
  raw counts for any other data set.


