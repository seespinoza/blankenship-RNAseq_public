install.packages('gplots')
install.packages('heatmap.plus')
install.packages('RColorBrewer')

library('gplots')
library('heatmap.plus')
library('RColorBrewer')

# Read in DE data
DEvalues <- read.csv('merged_YS_ctl_ALL.csv', row.names = 1, header = TRUE)
input <- as.matrix(DEvalues)

# Change all NA values to zero
input[is.na(input)] <- 0

# Generate heatmap
heatmap.2(input, trace ='none', density='none', col=bluered(20), cexRow=1, cexCol=1.2, scale='row', dendrogram = 'column', labRow = '')

