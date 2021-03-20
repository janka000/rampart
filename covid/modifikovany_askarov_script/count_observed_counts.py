import argparse
import sys

import pysam

from helpers import load_fasta, apply_to_cigartuples, create_barcodes_dict, print_alignments

letters = "ACGT"
l2n = {letter: num for num, letter in enumerate(letters)}

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=str)
    parser.add_argument("alignment", type=str)
    parser.add_argument("csv", type=str)
    parser.add_argument("-o", "--output", type=str, required=True)
    parser.add_argument("--alignment_low_cutoff", type=int, default=50)
    return parser.parse_args(argv)

def dump_observed_counts(counts, f):
    #position, barcode, A, C, G, T
    for barcode in counts:
       for position, pos_counts in enumerate(counts[barcode]):
           print(f"{position+1},{barcode},{pos_counts[0]},{pos_counts[1]},{pos_counts[2]},{pos_counts[3]}", file=f)

"""
def dump_observed_counts(counts_by_pos, f):
    print("position,letter,count", file=f)
    for position, counts in enumerate(counts_by_pos):
        for i, letter in enumerate("ACGT"):
            print(f"{position+1},{letter},{counts[i]}", file=f)

def dump_observed_counts_for_barcodes(counts_by_barcodes_and_pos, f):
    for barcode in counts_by_barcodes_and_pos:
        fname = barcode+".txt"
        with open(fname, "w") as barcodefile:
            dump_observed_counts(counts_by_barcodes_and_pos[barcode], barcodefile)
"""            

def count_bases_in_alignment(alignments, reference, alignment_length_low_cutoff, barcodes_dict):
    global l2n
    counts_by_pos = [[0 for _ in letters] for _ in reference]
    empty_queries_count = 0
    short_alignments_count = 0
    counts_by_barcode_and_pos = {}
    counts_by_barcode_and_pos["none"] = [[0 for _ in letters] for _ in reference]

    def count_alongside_cigar(op, l, r, q, al, barcode):
        global l2n
        nonlocal counts_by_pos, reference
        query = al.query_sequence
        if op == 0 or op == 7 or op == 8:
            for k in range(l):
                try:
                    counts_by_pos[r + k][l2n[query[q + k]]] += 1
                    counts_by_barcode_and_pos[barcode][r + k][l2n[query[q + k]]]+=1
                except IndexError as e:
                    print(e)
                    print(f"{op},{l},{r + k}<?{len(counts_by_pos)},{q + k}<?{len(query)}")
                    sys.exit(1)
                    
    for alignment_num, alignment in enumerate(alignments.fetch()):
        query = alignment.query_sequence
        if query is None:
            empty_queries_count += 1
            print(f"{empty_queries_count} empty queries so far! ({alignment_num} processed)")
            continue
        alignment_length = alignment.query_alignment_length
        if alignment_length < alignment_length_low_cutoff:
            short_alignments_count += 1
            print(f"{short_alignments_count} short alignments so far! ({alignment_num} processed)")
            continue
        query_name = alignment.query_name
        if query_name in barcodes_dict:
            barcode = barcodes_dict[query_name]
            #print(barcode)
            if not barcode in counts_by_barcode_and_pos:
                print("found new barcode! "+barcode)
                counts_by_barcode_and_pos[barcode] = [[0 for _ in letters] for _ in reference]
        else:
            barcode = "none"
            print(barcode)
        apply_to_cigartuples(count_alongside_cigar, alignment, barcode)
    return counts_by_pos, counts_by_barcode_and_pos


def count_observed_counts(reference_filename,
                          alignment_filename,
                          csv_filename,
                          output_filename,
                          alignment_length_low_cutoff):
    reference = list(load_fasta(reference_filename))[0][1] 
    alignments = pysam.AlignmentFile(alignment_filename, "rb")
    #print_alignments(alignments)
    barcodes_dict = create_barcodes_dict(csv_filename)
    #print(barcodes_dict)

    counts_by_pos, counts_by_barcode_and_pos = count_bases_in_alignment(alignments, reference, alignment_length_low_cutoff, barcodes_dict)

    with open(output_filename, "w") as f:
        dump_observed_counts(counts_by_barcode_and_pos, f)
        #dump_observed_counts(counts_by_pos, f)
    #dump_observed_counts_for_barcodes(counts_by_barcode_and_pos, f)


def main():
    args = parse_args(sys.argv[1:])
    count_observed_counts(reference_filename=args.reference,
                          alignment_filename=args.alignment,
                          csv_filename=args.csv,
                          output_filename=args.output,
                          alignment_length_low_cutoff=args.alignment_low_cutoff)


if __name__ == "__main__":
    main()
