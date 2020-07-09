from Bio import Entrez

refList = ['NC_032089.1', 'NC_032090.1', 
           'NC_032091.1', 'NC_032092.1', 
           'NC_032093.1', 'NC_032094.1', 
           'NC_032095.1', 'NC_032096.1']

genes = open('genes.txt', 'r')
gList = []


#testFile = open('testFile.txt', 'w')
Entrez.email = 'se.espinoza132@gmail.com'
Entrez.api_key = '21f9bebb6c243e6f7cdb3e38e088012b0709'
#handle = Entrez.efetch(db="nuccore", id="NC_032090.1", rettype="gbwithparts", retmode="text")

#for line in handle:
#    testFile.write(line)

for refseq in refList:
    handle = Entrez.efetch(db="nuccore", id=refseq, rettype="gbwithparts", retmode="text")
    with open(refseq, 'w') as f:
        for line in handle:
            f.write(line)

#testFile.close()


for gene in genes:
    gList.append(gene.strip('\n'))

def buildDict():
    dico = {}
    switch = False

    for ref in refList:
        with open(ref, 'r') as f:
            temp = []
            rnaID = ''
            for line in f:
                if ('     CDS' in line or '     gene' in line) and switch:
                     seq = ''
                     count = 0
                     if rnaID:
                         handle = Entrez.efetch(db="nuccore", id=rnaID, rettype="fasta", retmode="text")
                         for line in handle:
                             if count > 0:
                                 seq += line.strip('\n')
                             count += 1
                     switch = False
                     dico.update({tuple(temp):seq})
                     print(temp)

                     temp = []
                     rnaID = ''

                if switch and '/gene=' in line:
                    temp.append(line.split('"')[1])

                if switch and '/locus_tag=' in line:
                    temp.append(line.split('"')[1])

                if switch and '/transcript_id=' in line:
                    rnaID = line.split('"')[1]

                if '     mRNA' in line:
                    switch = True

    return dico
def buildaa():
    aaFile = open('aa1.txt', 'r')
    codonDict = {}
    for line in aaFile:
        tempLine = (line.strip()).split('\t')
        x = tuple(tempLine[0].strip('"').split(', '))
        y = tempLine[1]
        codonDict.update({x: y})
    aaFile.close()
    return codonDict

def buildaaCount(cDict):
    countDict = {}
    for i in cDict:
        for codon in i:
            countDict.update({codon:0})
    return countDict
    
seqs = buildDict()

codDict = {}
codDict = buildaa()
outFile = open('codonCounts.csv', 'w')
def write_codons(seq, cDict):
    count = buildaaCount(cDict)
    codon = ''
    for i in range(len(seq) // 3):
        codon = seq[0+(i*3):3+(i*3)]
        for c in count:
            if c == codon:
                count.update({c:count[c] + 1})
                break

    return count

# Header
head = buildaaCount(codDict)
print(head)
for i in head:
    outFile.write(i + ',')
outFile.write('\n')


for entry in seqs:
    for gene in entry:
         outFile.write(gene + ',')
         break
    temp = write_codons(seqs[entry], codDict)
    for i in temp:
        outFile.write(str(temp[i]) + ',')
    outFile.write('\n')

outFile.close()
