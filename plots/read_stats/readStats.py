# script to extract uniquely mapped reads from STAR alignement files

import os

def write_stats(fname):
	percentage = ''
	readcounts = ''
	with open(fname, 'r') as f:
		for line in f:
			if 'Uniquely mapped reads' in line:
				readcounts = line.strip('\n').split('Uniquely mapped reads ')[1]
			if 'Uniquely mapped reads number' in line:
				percentage = line.strip('\n').split('Uniquely mapped reads number')[1]
		return readcounts, percentage
				


directory = '/work/blankenship/sespinoza/old_data/bash_scripts/readStats'
with open('readStats.txt', 'w') as f:
	for filename in os.listdir(directory):

		if filename.endswith('final.out'):
			print(filename)
			f.write(filename + '\n')
			temp = write_stats(filename)
			for x in temp:
				f.write(x + '\n')


