#Library for Differential Gene Expression Analysis
# (calculates fold change values)
library(DESeq2)
library(apeglm)
# Library for manipulating fold change values
library(rnaseqWrapper)

# columns of control group in counts
cols <- c(25, 26, 27)

# function to switch control groups to first column
switch_columns <- function(rawC, colls) {
	c <- 1
	for (coll in colls) {
		rawC[,c(c, coll)] <- rawC[,c(coll, c)]
		colnames(rawC)[c(c,coll)] <- colnames(rawC)[c(coll, c)]
		c <- c + 1
         }

return(rawC)
}

# experimental groups
expNames <- c('ctl', 'FS', 'LL', 'LS', 'RL', 'RS', 'SL', 'SS', 'FL', 'YS')

# function to create experiment meta data
create_metadata <- function(colnames) {
    x <- 'coldata <- data.frame(condition = factor(c('
    counter <- 0
    for (name in colnames) {
    if (counter == length(colnames) - 1) {
        temp <- paste('rep("',name,'",3)', sep='')
        x <- paste(x,temp,sep='')
        }
    else {
        temp <- paste('rep("',name,'",3),', sep='')
        x <- paste(x,temp,sep='')
        }
        counter <- counter + 1
    }
    x <- paste(x, ')))', sep='')
    return(eval(parse(text=x)))
}

# Read in raw count matrix
countdata <- read.table("finalTableLiquid.txt", header = TRUE, row.names = 1)

countdata <- switch_columns(countdata, cols)

# Set up experiment metadata
coldata <- create_metadata(expNames)

# Run DESeq2
dds <- DESeqDataSetFromMatrix(countData = countdata, colData = coldata, design =~ condition)

dds <- DESeq(dds, betaPrior= FALSE)

resultsNames(dds)

dds$Intercept

# function to create FC tables
create_FC_tables <- function(DEobj) {
    for (i in resultsNames(dds)[-1]) {
        tempRes <- lfcShrink(DEobj, coef=i, type='apeglm')
	tempMatrix <- tempRes['log2FoldChange']
	colnames(tempMatrix) <- c(i)
        write.csv(tempMatrix, file = paste(i,'.csv',sep=''))
        }
}

FC_tables <- create_FC_tables(dds)
FCdir <- '~/Documents/Blankenship/3_hour_sandbox/'

# All merged FC values
FCmerge <- mergeCountFiles(FCdir, fileID = '*csv', fileSep = ',', seqIDcol = 1, colsToKeep = c(2))
write.csv(FCmerge, file='merged30min.csv')
