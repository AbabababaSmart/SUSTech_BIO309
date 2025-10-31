## Preface

This guide focuses on processing and analyzing transcript data from the GENCODE release 49 dataset. The dataset contains genomic information about human transcripts, including their IDs, gene names, types, and lengths. 

| **Field** | **Meaning**                     | **Example**          |
| --------- | ------------------------------- | -------------------- |
| `$1`      | Transcript ID                   | ENST00000456328.2    |
| `$2`      | Gene ID                         | ENSG00000290825.1    |
| `$3`      | OTTHUMG or strand info (-or ID) | OTTHUMT00000362751.1 |
| `$4`      | OTTHUMT ID                      | DDX11L2-202          |
| `$5`      | Transcript name                 | DDX11L2              |
| `$6`      | Gene name                       | DDX11L2              |
| `$7`      | Transcript length (nt)          | 1657                 |
| `$8`      | Gene type                       | InCRNA               |


Using `awk`, various tasks will be performed, such as filtering specific categories (e.g., protein-coding genes), pattern matching, and generating summary statistics. The aim is to extract relevant information, classify transcripts by length, and compute distribution and average transcript length by gene type.


## Dataset download

```bash
wget –c https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_49/gencode.v49.transcripts.fa.gz
gunzip genc
```

## Command

### Part 1: Reading and Filtering Records

#### 1. Basic Extraction
```
awk '/^>/ { 
    FS="|"; 
    print $1, $6, $8 
}' gencode.v49.transcripts.fa
```

#### 2. Pattern Matching with Regular Expressions (Gene name starting with MT-, RPL, or RPS)
```
awk '/^>/ {
    FS="|"; 
    if ($6 ~ /^MT-|^RPL|^RPS/) 
        print $1, $6, $8 
}' gencode.v49.transcripts.fa
```

#### 3. Filtering by Biotype (Protein-Coding Transcripts)
```
awk '/^>/ {
    FS="|"; 
    if ($8 == "protein_coding") 
        count++ 
} END { 
    print "Total protein-coding transcripts:", count 
}' gencode.v49.transcripts.fa
```

### Part 2: Conditional Logic and Numeric Expressions

#### 4. Length-Based Classification (Short, Medium, Long)
```
awk '/^>/ {
    FS="|"; 
    if ($8 == "protein_coding") {
        if ($7 < 1000) 
            print $1, "short"; 
        else if ($7 >= 1000 && $7 <= 2000) 
            print $1, "medium"; 
        else if ($7 > 2000) 
            print $1, "long"; 
    }
}' gencode.v49.transcripts.fa
```

#### 5. Skipping Non-Protein-Coding Lines and Printing Line Number
```
awk '/^>/ {
    FS="|"; 
    if ($8 != "protein_coding") 
        next; 
    print NR, $1, $6, $8 
}' gencode.v49.transcripts.fa
```

### Part 3: Arrays and Summary Statistics

#### 6. Transcript Count Per Gene (Protein-Coding)
```
awk '/^>/ {
    FS="|"; 
    if ($8 == "protein_coding") 
        gene_count[$2]++ 
} END { 
    for (gene in gene_count) 
        print gene, gene_count[gene] 
}' gencode.v49.transcripts.fa
```

#### 7. Transcript Type Distribution
```
awk '/^>/ {
    FS="|"; 
    type_count[$8]++ 
} END { 
    for (type in type_count) 
        print type, type_count[type] 
}' gencode.v49.transcripts.fa
```

#### 8. Average Transcript Length per Gene Type
```
awk '/^>/ {
    FS="|"; 
    length_sum[$8] += $7; 
    count[$8]++ 
} END { 
    for (type in length_sum) 
        printf "%s: %.2f\n", type, length_sum[type] / count[type] 
}' gencode.v49.transcripts.fa
```