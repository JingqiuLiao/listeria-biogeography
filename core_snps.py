#!/usr/bin/env python
# 04/29/2017
# Jingqiu Liao
# Remove duplicated sites and get SNPs from an alignment.
# Install Bio and multiprocess before running.
# Run `pip install biopython` to install Bio.
# Run `pip install multiprocess` to install multiprocess.

import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import single_letter_alphabet
from multiprocess import Pool

num_threads = 1
in_file = ""
out_file = "no_dup_seq.fasta"
sequences = []


def usage():
    '''
    Print out usage.
    '''
    print("Usage: %s [-n NUM_THREADS] [-o OUT_FILE] FASTA_FILE" % sys.argv[0])


def progress():
    '''
    Print a dot ('.') immediately to show the process is not dead.
    '''
    sys.stdout.write('.')
    sys.stdout.flush()


def parse_args():
    '''
    Process arguments.
    '''
    global num_threads
    global in_file
    global out_file

    # check the number of arguments
    if len(sys.argv) % 2 != 0:
        usage()
        sys.exit(-1)

    try:
        for i in range(1, len(sys.argv), 2):
            if sys.argv[i] == '-n':
                num_threads = int(sys.argv[i + 1])
            elif sys.argv[i] == '-o':
                out_file = sys.argv[i + 1]

        # set input FASTA file
        in_file = sys.argv[len(sys.argv) - 1]

    except Exception:
        # in case anything going wrong during the argument processing
        usage()
        sys.exit(-1)


def find_nondup(site):
    '''
    Find non-duplicate sites.
    Return None if all samples share an identical site.
    '''
    global sequences

    # show progress every 5000 sites
    if site % 5000 == 0:
        progress()

    c = ""
    for seq_record in sequences:
        if c == "":
            c = seq_record[site]
        elif c != seq_record[site]:
            return site
    return None


if __name__ == '__main__':
    # parse arguments
    parse_args()

    # record the sequences and the number of sites
    # make sure the num of sites are identical across all samples
    num_sites = 0
    for seq_record in SeqIO.parse(in_file, "fasta"):
        assert num_sites == 0 or num_sites == len(seq_record)
        sequences.append(seq_record)
        num_sites = len(seq_record)

    # compute the non-duplicate site indices
    # speed up by multi-threading
    thread_pool = Pool(num_threads)
    result = thread_pool.map_async(find_nondup, range(num_sites))
    non_dup_indices = [x for x in result.get() if x is not None]

    # generate and write out new sequences according to the indices
    with open(out_file, "w") as handle:
        for seq_record in sequences:
            new_seq = thread_pool.map(seq_record.__getitem__, non_dup_indices)
            record = SeqRecord(Seq("".join(new_seq), single_letter_alphabet),
                    id=seq_record.id, name=seq_record.name,
                    description=seq_record.description)
            SeqIO.write(record, handle, "fasta")
    print("Done! Hooray!")
