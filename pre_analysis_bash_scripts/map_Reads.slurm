#!/bin/sh
#SBATCH --job-name=map_Reads
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=168:00:00
#SBATCH --mem=64gb
#SBATCH --output=map_Reads%J.out
#SBATCH --error=map_Reads%J.err

# All media names distinguished by solid/liquid suffix
declare -a media=("YDP_solid" "Spider_solid" "FBS_solid" "Lees_solid" "RPMI_solid"
                "YDP_liquid" "Spider_liquid" "FBS_liquid" "Lees_liquid" "RPMI_liquid")

# sample letter
declare -a letter=("_a" "_b" "_c")

declare -i counter=27

# Base directory for all data
baseDir='/work/blankenship/sespinoza/old_data'

# The root SRR number
rootSRR='SRR56658'

# fastq suffix
s='.fastq'

# Load the STAR enviroment
module load star/2.7

# Iterate through all media samples there will be 2 runs per letter
# (i.e. SRR5665827 and SRR5665827 will both correspond to YDP_solid_a)
for i in "${media[@]}"
do
  for x in "${letter[@]}"
  do

    STAR --runThreadN 30 \
         --genomeDir $baseDir/genomeIndices \
         --readFilesIn  $baseDir/old_reads/$rootSRR$counter$s,$baseDir/old_reads/$rootSRR$((counter+1))$s \
         --outFileNamePrefix $i$x

    counter=$((counter+2))
  done
done

