import os
import sys
import argparse

from helpers import load_fasta, dump_dict_to_file

merged_dict={}
letters = "ACGT"

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str)
    parser.add_argument("reference", type=str)
    parser.add_argument("output", type=str)
    return parser.parse_args(argv)

def load_files_to_dict(directory_path, reference):
    print("directory path: ", directory_path)
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"): 
            print(os.path.join(directory_path, filename))
            load_file(os.path.join(directory_path, filename), reference)
            continue
        else:
            continue

def load_file(file_path, reference):
    global merged_dict
    with open(file_path, "r") as f:
        for line in f:
            l = line.split(",")
            position = int(l[0])-1
            barcode = l[1]
            A = int(l[2])
            C = int(l[3])
            G = int(l[4])
            T = int(l[5])
            if not barcode in merged_dict:
                print("found new barcode! "+barcode)
                merged_dict[barcode] = [[0 for _ in letters] for _ in reference]
            merged_dict[barcode][position][0]+=A
            merged_dict[barcode][position][1]+=C
            merged_dict[barcode][position][2]+=G
            merged_dict[barcode][position][3]+=T    
    
    
def main():
    args = parse_args(sys.argv[1:])   
    reference = list(load_fasta(args.reference))[0][1]
    load_files_to_dict(args.directory, reference)
    with open(args.output, "w+") as f:
        dump_dict_to_file(merged_dict,f)
    
if __name__ == "__main__":
    main()
    
