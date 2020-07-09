# Get gene sets from sig gene set
# Assumes ctl twin is first column in gene set

import sys
import getopt

inputFile = ''
outputFile = ''
prefix = ''
bufferNo = 0
sampleNames = []

# Function name: usage
# Description: Prints out error message if invalid options are entered
def usage():
    print('\nUsage: [-i FILE] [-b BUFFER] [-p OUTPUT PREFIX]')
    print('-i: list of file names containing log change data')
    print('-b: Buffer gene number; must be a positive integer')
    print('-p: Output file prefixes')
 # Read in the command-line arguments into the opts list.
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:b:p:")

except getopt.GetoptError as err:
    # Redirect STDERR to STDOUT (insures screen display)
    sys.stdout = sys.stderr

    # Print help information
    print(str(err))

    # Print usage information; usage() is the name of a
    # function (declared elsewhere) that displays usage
    # information (just a series of print statements).
    usage()

    # Exit the program
    sys.exit(2)

    # Process the opt and arg lists displaying the argument of
    # each option.

for (opt, arg) in opts:
    if opt == '-i':
        inputFile = arg
    if opt == '-b':
        bufferNo = int(arg) 
    if opt == '-p':
        prefix = arg

if not inputFile:
    usage()
    sys.exit(2)
else:
    inFile = open(inputFile, 'r')

if not prefix:
    usage()
    sys.exit(2)
else:
    downFile = open(prefix + 'downFile.csv', 'w')
    upFile = open(prefix + 'upFile.csv', 'w')

def getGeneSet(geneRecord, buff):
    counter = 0
    log2count = 0
    gRecord = geneRecord[1:] # Removes gene name
    threshHold = len(gRecord) - 1 - buff # min amount of log2count
    # Validate UpGenes
    for log2 in gRecord:
        if counter == 0 and (float(log2) > -1 and float(log2) != -27000):
            break
        if counter > 0 and (float(log2) > 1): # Count True cases
            log2count += 1
        counter += 1

    if threshHold <= log2count:
        return geneRecord[0], ''
    # Valid DownGenes
    counter = 0
    log2count = 0
    for log2 in gRecord:
        if counter == 0 and (float(log2) < 1 and float(log2) != -27000):
            break
        if counter > 0 and (float(log2) < -1 and float(log2) != -27000):
            log2count += 1
        counter += 1

    if threshHold <= log2count:
        return '', geneRecord[0]
    return '', ''
verifyUp = open(prefix + 'verifyUp.txt', 'w')
verifyDown = open(prefix + 'verifyDown.txt', 'w')   

def build_dico(DEfile, buff):
    counter = 0
    geneUp = ''
    geneDown = ''
    dico = {}
    revisedList = []
    geneListUp = []
    geneListDown = []
    # iterate through merged file and get send each record to compare func
    for line in DEfile:
        if counter != 0:
            tempLine = line.strip('\n').split(',')
            for i in tempLine:
                if i == 'NA':
                    revisedList.append('-27000') # Dummy value signifying NA
                else:
                    revisedList.append(i)  
            geneUp, geneDown = getGeneSet(revisedList, buff)
            revisedList = []
            if geneUp:
                geneListUp.append(geneUp)
                verifyUp.write(line + '\n')
            elif geneDown:
                geneListDown.append(geneDown)
                verifyDown.write(line + '\n')
            geneUp = ''
            geneDown = ''
        counter += 1
    return geneListUp, geneListDown


geneListUp, geneListDown = build_dico(inFile, bufferNo)

verifyUp.close()
verifyDown.close()
# Print results to std out
count = 0
for gene in geneListUp:
    if count == len(geneListUp) - 1:
        upFile.write(gene.strip('"'))
    else:
        upFile.write(gene.strip('"') + '\n')

count = 0
for gene in geneListDown:
    if count == len(geneListDown) -1:
        downFile.write(gene.strip('"'))
    else:
        downFile.write(gene.strip('"') + '\n')

    
upFile.close()
downFile.close()
inFile.close() 
