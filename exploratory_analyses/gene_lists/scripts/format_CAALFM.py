import sys
import getopt

inputFile = ''
outputFile = ''
# Function name: usage
# Description: Prints out error message if invalid options are entered
def usage():
    print('\nUsage: sespinoza_Assign5.py [-i FILE] [-o FILE]')
    print('-i: input file list of geneIDs or  (CSV)')
    print('-o: output file (tab-delimited); else stdout')
 # Read in the command-line arguments into the opts list.
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:o:g")

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
    if opt == '-o':
        outputFile = arg

if not inputFile:
    usage()
    sys.exit(2)
else:
    inFile = open(inputFile, 'r')

if not outputFile:
    outFile = sys.stdout
else:
    outFile = open(outputFile, 'w')

for gene in inFile:
    temp = gene.strip('\n')
    if 'CAALFM' in gene:
        temp = temp.replace('CAALFM_', '')
        outFile.write(temp[0:2] + '_' + temp[2:8] + '_' + temp[8] +  '\n')
    else:
        outFile.write(temp +  '\n')

outFile.close()
inFile.close()
