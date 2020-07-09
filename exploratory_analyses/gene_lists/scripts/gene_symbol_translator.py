# Translates symbols to gene IDs for the Candida albicans strain SC5314

import sys
import getopt
import mygene

inputFile = ''
outputFile = ''
refList = []
genes = []
refFile = open('geneID_key.tab', 'r')
geneID = False

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

def build_refList():
    refList = []
    for record in refFile:
         tempLine = record.strip('\n')
         tempLine = tempLine.split('\t')
         refList.append(tempLine)
    return refList

def buildInput_list():
    geneSymbols = []
    for gen in inFile:
        temp = gen.strip('\n')
        geneSymbols.append(temp)
    return geneSymbols

genes = buildInput_list()
biggestID  = ''
biggestScore = 0

for gene in genes:
    mg = mygene.MyGeneInfo()
    try:
        res = mg.query(gene,scopes=['symbol','alias','name'], fields=['symbol'], species='237561', verbose=False)
    except:
        outFile.write(gene + '\n')
    if res['total'] != 0:
        if res['total'] > 1:
            biggestID = res['hits'][0]['symbol']
            biggestScore = res['hits'][0]['_score']
            for hit in res['hits']:
                if hit['_score'] > biggestScore:
                    biggestScore = hit['_score']
                    biggestID = hit['symbol']
            outFile.write(biggestID + '\n')
        else:
            outFile.write(res['hits'][0]['symbol'] + '\n')
    else:
        print(gene + 'NA\n')

inFile.close()
outFile.close()



