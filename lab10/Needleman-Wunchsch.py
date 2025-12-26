def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    # Initialize DP matrix
    len1, len2 = len(seq1), len(seq2)
    dp_matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    
    # Fill the first row and first column with gap penalties
    for i in range(1, len1 + 1):
        dp_matrix[i][0] = gap * i
    for j in range(1, len2 + 1):
        dp_matrix[0][j] = gap * j
    
    # Fill the DP matrix using the recurrence relation
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            match_or_mismatch = dp_matrix[i-1][j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            delete = dp_matrix[i-1][j] + gap
            insert = dp_matrix[i][j-1] + gap
            dp_matrix[i][j] = max(match_or_mismatch, delete, insert)
    
    # Traceback to find the final alignment
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = len1, len2
    
    while i > 0 and j > 0:
        current_score = dp_matrix[i][j]
        diagonal_score = dp_matrix[i-1][j-1]
        up_score = dp_matrix[i-1][j]
        left_score = dp_matrix[i][j-1]
        
        if current_score == diagonal_score + (match if seq1[i-1] == seq2[j-1] else mismatch):
            aligned_seq1.append(seq1[i-1])
            aligned_seq2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif current_score == up_score + gap:
            aligned_seq1.append(seq1[i-1])
            aligned_seq2.append('-')
            i -= 1
        else:
            aligned_seq1.append('-')
            aligned_seq2.append(seq2[j-1])
            j -= 1
    
    # If any sequence is left, align with gaps
    while i > 0:
        aligned_seq1.append(seq1[i-1])
        aligned_seq2.append('-')
        i -= 1
    while j > 0:
        aligned_seq1.append('-')
        aligned_seq2.append(seq2[j-1])
        j -= 1
    
    # Reverse the alignments 
    aligned_seq1 = ''.join(reversed(aligned_seq1))
    aligned_seq2 = ''.join(reversed(aligned_seq2))
    
    print("DP Matrix:")
    for row in dp_matrix:
        print(row)
    print("\nAlignment Score:", dp_matrix[len1][len2])

if __name__ == "__main__":
    seq1 = "GATTACA"
    seq2 = "GCATGCU"
    needleman_wunsch(seq1, seq2)
