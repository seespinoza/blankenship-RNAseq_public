#!/bin/sh
#SBATCH --job-name=get_Raw_Counts
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=168:00:00
#SBATCH --mem=64gb
#SBATCH --output=get_Raw_Counts%J.out
#SBATCH --error=get_Raw_Counts%J.err

# Base directory for all data
baseDir='/work/blankenship/sespinoza/old_data'

# change directory to featureCounts tool directory
cd $WORK/tools/subread/bin

# Run featureCounts tool (minimum parameters)
./featureCounts -a $baseDir/gtfAnnotation/GCF_000182965.3_ASM18296v3_genomic.gtf \
                -o 30_minute_counts.txt \
		# Need to have converted C. albicans gff notation into gtf
		# using gffread to be able to use "-g gene_name" option.
		# Refer to convert_GFF_to_GTF.slurm for more info.
		-g gene_name \
                $baseDir/samFiles/*.sam
