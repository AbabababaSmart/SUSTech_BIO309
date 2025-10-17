#!/bin/bash

FA="hg38.fa"

#-------------------------------
# Task 1: 基本检查
#-------------------------------
check_file() {
    if [[ ! -f "$FA" ]]; then
        echo "Error: $FA not found!"
        exit 1
    fi
    echo "File name: $FA"
    echo "File size: $(du -h $FA | cut -f1)"
    echo "Number of lines: $(wc -l < $FA)"
    echo "First 5 lines:"
    head -n 5 $FA
}

#-------------------------------
# Task 2: 统计N
#-------------------------------
count_Ns() {
    local chrom=$1
    if [[ -z "$chrom" ]]; then
        # 全基因组N
        total=$(grep -v "^>" $FA | grep -oi "n" | wc -l)
        echo "Total N bases: $total"
    else
        # 指定染色体N
        count=$(awk -v chr=">$chrom" '
            BEGIN {found=0}
            /^>/ {found=($1==chr)?1:0; next}
            found {print}
        ' $FA | grep -oi "n" | wc -l)
        echo "Chromosome: $chrom"
        echo "Action: Ns"
        echo "Result: $count"
    fi
}

# 所有染色体 N 表格
count_Ns_all() {
    echo -e "Chromosome\tN_count"
    awk '
        /^>/ {chr=substr($1,2); next}
        {
            n=gsub(/[Nn]/,"")
            counts[chr]+=n
        }
        END {
            for (c in counts) {
                print c "\t" counts[c]
            }
        }
    ' $FA | column -t
}

#-------------------------------
# Task 3: 染色体长度
#-------------------------------
chrom_length() {
    local chrom=$1
    seq=$(awk -v chr=">$chrom" '
        BEGIN {found=0}
        /^>/ {found=($1==chr)?1:0; next}
        found {print}
    ' $FA)

    total=$(echo "$seq" | tr -d '\n' | wc -c)
    Ns=$(echo "$seq" | grep -oi "n" | wc -l)
    perc=$(awk -v n=$Ns -v t=$total 'BEGIN {printf "%.2f", (n/t*100)}')

    echo "Chromosome: $chrom"
    echo "Action: length"
    echo "Total bases: $total"
    echo "N count: $Ns"
    echo "% Ns: $perc"
}

# 所有染色体长度 + %N 表格
chrom_length_table() {
    local find_max=$1
    echo -e "Chromosome\tLength\tN_count\t%Ns"

    awk -v find_max=$find_max '
        /^>/ {
            if (chr!="") {
                perc=(total>0)?(Ns/total*100):0
                printf "%s\t%d\t%d\t%.4f\n", chr, total, Ns, perc
                if (perc > best_perc) {
                    best_chr=chr
                    best_perc=perc
                }
            }
            chr=substr($1,2)
            total=0; Ns=0
            next
        }
        {
            total+=length($0)
            n=gsub(/[Nn]/,"")
            Ns+=n
        }
        END {
            if (chr!="") {
                perc=(total>0)?(Ns/total*100):0
                printf "%s\t%d\t%d\t%.4f\n", chr, total, Ns, perc
                if (perc > best_perc) {
                    best_chr=chr
                    best_perc=perc
                }
            }
            if (find_max==1) {
                printf "\nChromosome with highest %%Ns: %s (%.4f %%)\n", best_chr, best_perc
            }
        }
    ' $FA | column -t
}

#-------------------------------
# Task 4: 提取子序列
#-------------------------------
extract_subseq() {
    local chrom=$1
    local start=$2
    local end=$3
    local out=$4

    if [[ -z "$chrom" || -z "$start" || -z "$end" ]]; then
        echo "Error: subseq requires chromosome, start, and end"
        exit 1
    fi
    if (( start < 1 || end <= start )); then
        echo "Error: invalid start/end"
        exit 1
    fi

    seq=$(awk -v chr=">$chrom" '
        BEGIN {found=0}
        /^>/ {found=($1==chr)?1:0; next}
        found {print}
    ' $FA | tr -d '\n')

    subseq=${seq:$((start-1)):$((end-start+1))}

    header=">$chrom:${start}-${end}"
    echo "$header" > "$out"
    echo "$subseq" >> "$out"

    echo "Subsequence written to $out"
    echo "First 10 bases:"
    echo "$header"
    echo "${subseq:0:10}..."
}

#-------------------------------
# Task 5: 参数解析
#-------------------------------
usage() {
    echo "Usage: $0 -c CHROM -a ACTION [-s START -e END -O OUTPUT]"
    echo "Actions:"
    echo "  check       : check file basic info"
    echo "  Ns          : count N bases (whole genome or one chromosome)"
    echo "  NsAll       : count N bases for all chromosomes (table)"
    echo "  length      : chromosome length + %Ns (one chromosome)"
    echo "  lengthAll   : chromosome lengths for all chromosomes (table)"
    echo "  maxNs       : chromosome with highest %Ns"
    echo "  subseq      : extract subsequence"
    exit 1
}

while getopts "c:a:s:e:O:" opt; do
    case $opt in
        c) chrom=$OPTARG ;;
        a) action=$OPTARG ;;
        s) start=$OPTARG ;;
        e) end=$OPTARG ;;
        O) output=$OPTARG ;;
        *) usage ;;
    esac
done

case $action in
    check) check_file ;;
    Ns) count_Ns "$chrom" ;;
    NsAll) count_Ns_all ;;
    length) chrom_length "$chrom" ;;
    lengthAll) chrom_length_table 0 ;;
    maxNs) chrom_length_table 1 ;;
    subseq) extract_subseq "$chrom" "$start" "$end" "${output:-${chrom}_${start}_${end}.fa}" ;;
    *) usage ;;
esac
