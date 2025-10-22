# hg38_tool.sh Usage Guide

This script is a **FASTA file processing tool**, primarily designed for the human genome reference sequence `hg38.fa`. It provides functionality for file checking, N base statistics, chromosome length calculation, and subsequence extraction.

---

## System Requirements
- Linux/Unix environment, supports Bash
- The system must have the following common commands: `grep`, `awk`, `wc`, `head`, `du`, `tr`, `column`, `bc`

Download the script and grant it executable permissions:
```bash
chmod +x hg38_tool.sh
```

## Download the FASTA file

```bash
wget -c https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/hg38.fa.gz
gunzip hg38.fa.gz
```

## Usage

```
./hg38_tool.sh -a ACTION [Other Parameters] 
```

#### Parameter Explanation:

  - **-a ACTION**  (Required) Specify the action to perform:
    - **check**    : Check basic information of the `hg38.fa` file  
    - **Ns**       : Count N bases (for the entire genome or a single chromosome)  
    - **NsAll**    : Output a table of N base counts for all chromosomes  
    - **length**   : Calculate the length, N count, and %Ns of a specific chromosome  
    - **lengthAll**: Output a table of lengths, N counts, and %Ns for all chromosomes  
    - **maxNs**    : Identify the chromosome with the highest %Ns  
    - **subseq**   : Extract a subsequence  

  - **-c CHROM**  Specify the chromosome name (e.g., `chr1`, `chr2`)  
  - **-s START**  Start position for subsequence extraction (1-based)  
  - **-e END**    End position for subsequence extraction  
  - **-O OUTPUT** Output filename (Optional, default is `chrX_start_end.fa`)




## Usage Examples

### 1. File Check
```
./hg38_tool.sh -a check
```

Output:
```
File name: hg38.fa
File size: 3.1G
Number of lines: 64186394
First 5 lines:
>chr1
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
```

### 2. Count N Bases
#### Entire Genome:
```
./hg38_tool.sh -a Ns
```

Output:
```
Total N bases: 159970322
```

#### Specific Chromosome:
```
./hg38_tool.sh -a Ns -c chr1
```
Output:
```
Chromosome: chr1
Action: Ns
Result: 18475410
```
#### All Chromosomes:
```
./hg38_tool.sh -a NsAll
```
Output:
```
Chromosome      N_count
chrUn_KI270528v1         0
chr20_GL383577v2_alt     0
chr15_GL383555v2_alt     0
…
```

### 3. Chromosome Length and %Ns
#### Single Chromosome:
```
./hg38_tool.sh -a length -c chr2
```
Output:
```
Chromosome: chr2
Action: length
Total bases: 242193529
N count: 1645301
% Ns: 0.68
```

#### All Chromosomes Table:
```
./hg38_tool.sh -a lengthAll
```
Output: 
```
Chromosome      Length  N_count %Ns
…
chrX                     156040895  1147866   0.7356
chrY                     57227415   30812372  53.8420
chrY_KI270740v1_random   37240      0         0.0000
```
#### Identify Chromosome with Highest %Ns:
```
./hg38_tool.sh -a maxNs
```
Output:
```
Chromosome      Length  N_count %Ns
…
chrX                     156040895  1147866   0.7356
chrY                     57227415   30812372  53.8420
chrY_KI270740v1_random   37240      0         0.0000
Chromosome               with       highest   %Ns:     chrUn_KI270317v1  (90.3847  %)
```

#### 4. Extract Subsequence
```
./hg38_tool.sh -a subseq -c chr3 -s 1000 -e 1100 -O chr3_region.fa
```
Output:
```
First 10 bases:
>chr3:1000-1100
NNNNNNNNNN...
```
Generated `chr3_region.fa` File Content:
```
>chr3:1000-1100
NNNNNNNNNN……
```

## Notes

### 1. Ensure the `hg38.fa` File Exists  
Before running the script, please ensure that the reference genome file **hg38.fa** is located in the same directory as the script. Otherwise, the script will throw an error and exit immediately.

### 2. Invalid Index Error Handling

When using the `-a subseq` action to extract a subsequence, the script will check if the input range is valid:

- The start position (`-s START`) must be **≥ 1**  
- The end position (`-e END`) must be **greater than the start position**  

If these conditions are not met, an error will be thrown and the script will exit. 
```
./hg38_tool.sh -a subseq -c chr1 -s 200 -e 100
```
