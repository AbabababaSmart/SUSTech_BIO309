import argparse
import re
from utils.codon_table import codon_table

# Reading FASTA & Inspecting Sequence Objects
def read_fasta(filename, debug=False):
    with open(filename, 'r') as file:
        sequences = []
        transcript_id = None
        sequence = ''
        
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if transcript_id:
                    sequences.append((transcript_id, sequence))
                transcript_id = line[1:].split('|')[0]  # Extract transcript ID
                sequence = ''
            else:
                sequence += line
        if transcript_id: 
            sequences.append((transcript_id, sequence))
    
    if debug:
        print(f"Total Sequences: {len(sequences)}")
        for transcript_id, seq in sequences:
            print(f"Transcript ID: {transcript_id}")
            print(f"Length of Sequence: {len(seq)}")
            print(f"First 50 bases: {seq[:50]}")
        
    return sequences

# Filtering by Length and GC Content
def calc_gc(seq):
    g = seq.count('G')
    c = seq.count('C')
    return (g + c) / len(seq) * 100

def filter_sequences(sequences, min_len=500, min_gc=40, max_gc=60, debug=False):
    selected_sequences = []
    for transcript_id, seq in sequences:
        gc_content = calc_gc(seq)
        if len(seq) >= min_len and min_gc <= gc_content <= max_gc:
            selected_sequences.append((transcript_id, seq, gc_content))
    
    if debug:
        print("\nSelected Sequences with GC Content:")
        for transcript_id, seq, gc_content in selected_sequences:
            print(f"Transcript ID: {transcript_id}, GC%: {gc_content:.2f}")
    
    return selected_sequences

# Find First ATG and Translate to Protein
def translate_dna(seq):
    protein = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i:i+3]
        aa = codon_table.get(codon, '')
        if aa == '*':  # Stop at stop codon
            break
        protein.append(aa)
    return ''.join(protein)

def find_first_atg(seq):
    return seq.find('ATG')

def process_selected_sequences(sequences, debug=False):
    proteins = []
    for transcript_id, seq, _ in sequences:
        start_pos = find_first_atg(seq)
        if start_pos != -1:
            protein = translate_dna(seq[start_pos:])
            proteins.append((transcript_id, start_pos + 1, protein))  # 1-based index for start
            
            if debug:
                print(f"Transcript ID: {transcript_id}, Start ATG: {start_pos + 1}, Protein: {protein}, Length: {len(protein)}")
    
    return proteins

# Find Potential G4 RNA Structures
def find_g4(seq):
    seq = seq.replace('T', 'U')  # Convert DNA to RNA
    pattern = r'(G{3,}\w{1,7}){3}G{3,}' 
    for match in re.finditer(pattern, seq):
        yield match.start()

def count_g4_sequences(sequences, debug=False):
    g4_counts = []
    for transcript_id, seq, _ in sequences:
        g4_positions = list(find_g4(seq))
        if g4_positions:
            print(transcript_id)
            print(g4_positions)
            g4_counts.append((transcript_id, len(g4_positions)))
    
    if debug:
        print("\nG4 RNA Motif Counts:")
        for transcript_id, g4_count in g4_counts:
            print(f"Transcript ID: {transcript_id}, G4 Count: {g4_count}")
    
    return g4_counts

def main():
    parser = argparse.ArgumentParser(description="Analyze transcript sequences in FASTA format.")
    parser.add_argument('--input', required=True, help='Input FASTA file')
    parser.add_argument('--output', required=True, help='Output results file')
    parser.add_argument('--minlen', type=int, default=500, help='Minimum sequence length')
    parser.add_argument('--min_gc', type=float, default=0.4, help='Minimum GC content percentage')
    parser.add_argument('--max_gc', type=float, default=0.6, help='Maximum GC content percentage')
    parser.add_argument('--debug', action='store_true', help='Enable print output')
    
    args = parser.parse_args()

    # Read FASTA file
    sequences = read_fasta(args.input, args.debug)

    # Filter sequences based on length and GC content
    filtered_sequences = filter_sequences(sequences, args.minlen, args.min_gc * 100, args.max_gc * 100, args.debug)

    # Process and translate selected sequences
    proteins = process_selected_sequences(filtered_sequences, args.debug)

    # Find G4 RNA structures of selected sequences
    g4_counts = count_g4_sequences(filtered_sequences, args.debug)

    with open(args.output, 'w') as out_file:
        out_file.write("Transcript_ID\tStart_ATG_Position\tProtein_Sequence\n")
        for transcript_id, start_pos, protein in proteins:
            out_file.write(f"{transcript_id}\t{start_pos}\t{protein}\n")

        out_file.write("\nG4 RNA Motif Counts:\n")
        for transcript_id, g4_count in g4_counts:
            out_file.write(f"{transcript_id}\t{g4_count}\n")

if __name__ == '__main__':
    main()
