#!/bin/sh
#SBATCH --job-name=sra_dl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=168:00:00
#SBATCH --mem=32gb
#SBATCH --output=/work/blankenship/sespinoza/old_data/sra_dl%J.out
#SBATCH --error=/work/blankenship/sespinoza/old_data/sra_dl%J.err

CDir='/work/blankenship/sespinoza/old_data'
cd $CDir
module load anaconda

conda activate sra

python3 run_sra.py
