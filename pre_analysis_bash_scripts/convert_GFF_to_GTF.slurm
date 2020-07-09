#!/bin/sh
#SBATCH --job-name=convert_GFF_to_GTF
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=168:00:00
#SBATCH --mem=32gb
#SBATCH --output=/work/blankenship/sespinoza/old_data/convert_GFF_to_GTF%J.out
#SBATCH --error=/work/blankenship/sespinoza/old_data/convert_GFF_to_GTF%J.err

CDir='/work/blankenship/sespinoza/tools/cufflinks'
cd $CDir

./gffread \
	GCF_000182965.3_ASM18296v3_genomic.gff \
	-T \
	-o GCF_000182965.3_ASM18296v3_genomic_gffread.gtf
