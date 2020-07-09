#!/bin/sh
#SBATCH --job-name=generate_Indices
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=168:00:00
#SBATCH --mem=64gb
#SBATCH --output=generate_Indices%J.out
#SBATCH --error=generate_Indices%J.err

# Base directory for all data
baseDir='/work/blankenship/sespinoza/old_data'

module load star/2.7

# Generating STAR genome indexes
STAR --runThreadN 30 --runMode genomeGenerate \
     --genomeDir $baseDir/genomeIndices \
     --genomeFastaFiles $baseDir/genomeFasta/GCF_000182965.3_ASM18296v3_genomic.fna \
     --sjdbGTFfile $baseDir/gtfAnnotation/GCF_000182965.3_ASM18296v3_genomic.gtf \
     --sjdbOverhang 99 \
     --genomeSAindexNbases 10
