#!/usr/bin/env python
# 1/23/2019
# Jingqiu Liao
# run sigB allelic typing using blastn for multiple inquiries and collect the best match for each inquiry 
# prerequisite: 1) makde database by running: makeblastdb -in sigB_reference_fasta_file -dbtype nucl; 2) install blastn
# sigB_reference_fasta_file can be obtained from Food Microbe Tracker: http://www.foodmicrobetracker.com/


import glob
import subprocess

# sigB allelic typing using blastn
for fseq in glob.glob("*.fasta"):
    output = fseq[:-6] + '_sigB_out.txt'
    subprocess.run(['blastn', '-db', 'sigBhaplotypes03202019.fas', '-query=' + fseq, '-out=' + output, '-evalue', '1e-100', '-perc_identity', '70', '-outfmt', '6 qacc sacc slen qstart qend sstart send qseq sseq mismatch gaps evalue bitscore length'])

# collect the hit with highest bitscore from the output of blastn
for fname in sorted(glob.glob("*.txt")):
    sum_line = []
    bitscore = []
    with open ('sigB_AT_result.txt', 'a') as g:
        with open(fname, 'r') as f:
            for line in f:
                sum_line.append(line.strip())
                bitscore.append(float(line.split()[12]))
            if len(bitscore) == 0:
                g.write (fname[:-13] + '\t' + '\n')
            else:
                lo = bitscore.index(max(bitscore))
                g.write(fname[:-13] + '\t' + sum_line[lo] + '\n')