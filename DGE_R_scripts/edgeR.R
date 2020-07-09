library(edgeR)

# Raw count data
datain <- read.delim("finalTable.txt", row.names="Geneid")

# experimental design
groups <-factor( c("YL", "YL", "YL", "FS", "FS", "FS", "LL", "LL", "LL", "LS", "LS", "LS", "RL", "RL", "RL", "RS", "RS", "RS", "SL", "SL", "SL", "SS", "SS", "SS", "FL", "FL", "FL", "YS", "YS", "YS"),
levels = c("YL", "FS", "LL", "LS"
, "RL", "RS", "SL", "SS", "FL", "YS"))


# create edgeR object
dgList <-DGEList(counts = datain, group=groups)


#Set ref level
dgList$samples$group <- relevel(dgList$samples$group, ref="YS")


# filter to retain genes that are represented at least 1 counts per million (cpm) in at least 2 samples
# OPTIONAL: not performed in DESeq2 analysis

countsPerMillion <- cpm(dgList)
countCheck <- countsPerMillion > 1
keep <- which(rowSums(countCheck) >= 2)
dgList <- dgList[keep,]
dgList$samples$lib.size <- colSums(dgList$counts)


# normalization using TMM method
dgList <- calcNormFactors(dgList, method="TMM")


# data exploration
# MDS plot
png("plotmds.png")
plotMDS(dgList, method="bcv", col=as.numeric(dgList$samples$group))
dev.off()

# Dispersion estimates
design.mat <- model.matrix(~dgList$samples$group)
colnames(design.mat) <- levels(dgList$samples$group)
dgList <- estimateGLMCommonDisp(dgList,design.mat)
dgList <- estimateGLMTrendedDisp(dgList,design.mat, method="power")
dgList <- estimateGLMTagwiseDisp(dgList,design.mat)
png("plotbcv.png")
plotBCV(dgList)
dev.off()

sampleList <- c("FS", "LS", "RS", "SS", "YL", "LL", "SL", "FL", "RL")
count <- 2
for(samp in sampleList) {
# Differential expression analysis
# Change coef variable to compare control to different sample
fit <- glmFit(dgList, design.mat)
lrt <- glmLRT(fit, coef=count)
edgeR_results <- topTags(lrt, n=Inf, sort.by = 'PValue')
write.csv(edgeR_results, file=paste('results_',samp,'.csv', sep=''))
count <- count + 1
}

# plot log2FC of genes and highlight the DE genes
deGenes <- decideTestsDGE(lrt, p=0.05)
deGenes <- rownames(lrt)[as.logical(deGenes)]
png("plotsmear.png")
plotSmear(lrt, de.tags=deGenes)
abline(h=c(-1, 1), col=2)
dev.off()

