## Usage Guide: Python Script for Sequence processing 


#### Step 1. Download the FASTA data
```bash
wget –c https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_49/gencode.v49.transcripts.fa.gz
gunzip gencode.v49.transcripts.fa.gz
```

#### Step 2. Run the script
```bash
python transcript_analyzer.py \
    --input /path/to/gencode.v49.transcripts.fa \
    --output /path/to/output_results.txt \
    --minlen 500 \
    --min_gc 0.4 \
    --max_gc 0.6 \
    --debug
```

Where:
- `--input`：Path to the input FASTA file.
- `--output`：Path to the output file where results will be saved.
- `--minlen`：Minimum sequence length, default value is 500.
- `--min_gc`：Minimum GC content, default is 0.4 (40%).
- `--max_gc`：Maximum GC content, default is 0.6 (60%).
- `--debug`：Enable debug output to show detailed processing information while running the script.


This command will read the `/path/to/gencode.v49.transcripts.fa` file, filter sequences with GC content between 40% and 60%, and length greater than 500. It will then find the ATG start codons in the selected sequences and translate them into protein sequences, while also counting the occurrence of G4 RNA structures. Finally, the analysis results will be saved in the `/path/to/output_results.txt file`.


To be more specific, the `output_results.txt` file will contain the following content:
```
Transcript_ID	Start_ATG_Position	Protein_Sequence
ENST00000832824.1	173	MPRVGWAIVHLLAPVVCM
ENST00000832825.1	169	MPRVGWAIVHLLAPVVCM
……

G4 RNA Motif Counts:
ENST00000831524.1	1
ENST00000831604.1	1
……
```
