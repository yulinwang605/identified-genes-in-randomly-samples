#!/usr/bin/env python2
######################################################################################################################################
#    The purpose of this script is to summarize the rarefaction curve of detected genes vs the number randomly selected samples.     #
#    CoverM (https://github.com/wwood/CoverM) was used to estimate the coverage values of genes in the reconstructed gene catalog    #
#    among different AS metagenomic data.                                                                                            #
#    If the gene coverage >= the provided cutoff, this gene would be deemed identified                                               #
#                                                                                                                                    #
#    Example files for input can be found in the folder of "example-data"                                                            #
#    This script was written and tested in python 2.7                                                                                #
######################################################################################################################################
__email__       = "yulinwang605@gmail.com"

import os
import random
import time

import sys, getopt

opts, args = getopt.getopt(sys.argv[1:], "hf:c:p:", ["folder=", "coverage=", "permution="])

def Usage():
    print ""
    print "Summarize identified genes in randomly select samples for the rarefaction curve"
    print ""
    print "-f   : Folder contains all CoverM (https://github.com/wwood/CoverM) results (contig-mode) of all all sample.."
    print "-c  : coverage cutoff for the valid identified genes in each sample."
    print "-p   : times of permution."
    print "-h  : Print help"
    print ""
    print ""

def finish():
    print""
    print"Job finidhed!"


for op, value in opts:
    if op == "-f":
        folder = value
        print "The folder of coverm results is ", folder
    elif op == "-c":
        filtercov = value
        print "Coverage cutoff is ", filtercov
    elif op == "-p":
        pm = value
        print "Use ", pm, " times permutation"
    elif op == "-h":
        Usage()
        sys.exit()

# relation = open("corresponding.txt","r")
output = open("samples-number-vs-identified-genes-" + str(pm) + "-permution.txt", "w")

output.write("Sample-names" + "\t" + "Number-of-samples" + "\t" + "Identified-genes" + "\n")

start = time.time()

# check sample number in the folder
onlyfiles = next(os.walk(folder))[2]
SampNum = len(onlyfiles)

# prefilter the coverm results to rm the undetected files
idName = {}
if os.path.exists("./filtered-coverm-results"):
    print "Coverm results have been filtered."
else:
    os.mkdir("./filtered-coverm-results")
    fileID = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            fileID += 1
            idName[str(fileID)] = str(file)
            tmp1 = open(os.path.join(root, file), "r")
            header = tmp1.readline()
            output1 = open("./filtered-coverm-results/" + str(file), "w")
            output1.write(str(header).strip() + "\n")
            for line in tmp1:
                if float(str(line).split("\t")[2]) >= float(filtercov):
                    output1.write(str(line).strip() + "\n")
                else:
                    continue
            output1.close()
print idName

# library of filename vs all identified genes.
allgenes = {}
for root, dirs, files in os.walk("./filtered-coverm-results"):
    for file in files:
        tmp2 = open(os.path.join(root, file), "r")
        header = tmp2.readline()
        tmplist = []
        for line in tmp2:
            tmplist.append(str(line).strip().split("\t")[1])
        allgenes[str(file).strip()] = tmplist[0] + "\t" + "\t".join(tmplist[1:])

# randomly select samples
ids = list(range(1, SampNum, 1))
for item in ids:
    for i in range(0, int(pm), 1):  # permutation times
        select = random.sample(ids, int(item))
        i += 1
        print "Randomly select ", item, "samples"
        filename = []
        genename = []
        for sampleid in select:
            filename.append(idName[str(sampleid)])
        for name in filename:
            genename = genename + str(allgenes[str(name)]).split("\t")
        uniqgname = list(set(genename))
        if len(filename) == 1:
            output.write(filename[0] + "\t" + str(item) + "\t" + str(len(uniqgname)) + "\n")
        else:
            output.write(filename[0] + " " + " ".join(filename[1:]) + "\t" + str(item) + "\t" + str(len(uniqgname)) + "\n")

output.close()

end = time.time()
print "Used time: ", str(end - start)

finish()
sys.exit()
