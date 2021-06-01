# identified-genes-in-randomly-samples
## General description 
We may obtain a non-redundant gene catalog from numbers of metagenomic datasets and want to draw a **rarefraction curve** of detected genes vs number of randomly selected metagenomic datasets.  

If we map the raw reads to the gene catalog (Nucleic acid sequences) using CoverM (contig mode), we will get a number of files that contain Gene Id and coverage.

## Input parameters
- `A folder contains all CoverM mapping results (**refer to the folder of example-data**).`  

- `Gene coverage cutoff (e.g., 0.5, gene coverage >0.5 was thought to be identified in given metagenomic dataset.)`

- `Times of permution （e.g., 3, randomly sampling 3 times）`

## Get help
```
  $ python summarize-identified-genes-in-randomly-selected-samples.py -h  
  
  
    -f : Folder contains all CoverM (https://github.com/wwood/CoverM) results (contig-mode) of all all sample.  
    -c : coverage cutoff for the valid identified genes in each sample.  
    -p : times of permution.  
    -h : Print help
```
## Example

```
  $ python summarize-identified-genes-in-randomly-selected-samples.py -f example-data -c 0.5 -p 3
```
