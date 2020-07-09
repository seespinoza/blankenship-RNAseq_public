
hr = ''
geneDico = {}
hr2 = ''

# Get all 3hr counts in dictionary
with open('3_hr_counts.txt', 'r') as f:
    counter = 0
    
    for line in f:
        if counter == 0:
            hr = line.strip('\n')

        else:
            tempLine = line.strip('\n').split('\t')
            geneDico.update({tempLine[0]:tempLine[1:]})
        counter += 1

# Get all 30 min counts in dictionary
with open('30_min_counts.txt', 'r') as f:
    counter = 0

    for line in f:
        tempLine = line.strip('\n').split('\t')
        
        if counter == 0:
            hr2 = line.strip('\n').split('\t', 1)[1]
 

        elif tempLine[0] in geneDico:
            for x in tempLine[1:]:
                geneDico[tempLine[0]].append(x)

        counter += 1

# Write to merged file
with open('merged_counts.txt', 'w') as f:
    counter = 0

    for i in geneDico:
        if counter == 0:
            print(hr2)
            f.write(hr + '\t' +  hr2 + '\n')

        f.write(i + '\t')
        tCount = 0
        for x in geneDico[i]:
            tCount += 1
            if tCount == len(geneDico[i]):
                f.write(x + '\n')
            else:
                f.write(x + '\t')
                    
        counter += 1
                




