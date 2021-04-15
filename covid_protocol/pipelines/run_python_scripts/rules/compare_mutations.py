import os
import sys
import argparse

from helpers import load_fasta, l2n

letters = "ACGT"

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    parser.add_argument("reference", type=str)
    parser.add_argument("mutations", type=str)
    parser.add_argument("--threshold", type=int, default=42) #minimal number of reads needed
    parser.add_argument("-o", "--output", type=str, required=True)
    return parser.parse_args(argv)
    
def load_file(file_path, reference):
    barcode_dict = {}
    with open(file_path, "r") as f:
        for line in f:
            l = line.split(",")
            position = int(l[0])-1
            barcode = l[1]
            A = int(l[2])
            C = int(l[3])
            G = int(l[4])
            T = int(l[5])
            if not barcode in barcode_dict:
                #print("found new barcode! "+barcode)
                barcode_dict[barcode] = [[0 for _ in letters] for _ in reference]
            barcode_dict[barcode][position][0]+=A
            barcode_dict[barcode][position][1]+=C
            barcode_dict[barcode][position][2]+=G
            barcode_dict[barcode][position][3]+=T   
    return barcode_dict


def load_mutations(mutations_path):    
    #nacitanie mut.txt
    
    mutations = {}
    sub_mutations = {}
    
    with open (mutations_path, "r") as txtfile:
        sub = False
        mut_name = ""
        for line in txtfile:
            line = line.strip()
            if line == "start_sub":
                sub = True
            elif line == "end_sub":
                sub = False
            elif sub:
                columns = line.split(" ")
                sub_mutations[mut_name].append([])
                index = len(sub_mutations)-1
                for i in range (2, len(columns)):
                    sub_mutations[mut_name][index].append(columns[i])
                
            elif not line.startswith('#') and line:
                columns = line.split(" ")
                mut_name = columns[0]
                mutations[mut_name] = []
                mutations[mut_name].append(int(columns[1]))
                mutations[mut_name].append([])
                for i in range(2, len(columns)):
                    mutations[mut_name][1].append(columns[i])
            

    return mutations
            
    
def guess(barcode_dict, mutacie, csv, threshold):
    #barcode dict - nacitany dictionary zo suboru (pocty ACGT na jednotlivych poziciach v jednotlivych barkodoch)
    #mutacie - nacitany subor mut.txt (load_mutations)
    #print(barcode_dict)
    print("barcode,strand,support,mutations,probability", file=csv)
    for barcode in barcode_dict:
        for strand in mutacie:
            probability = 0.0
            num_mut = 0
            pocet = 0
            support = []
            mutations_string = "" #mutacie sconcatenovane cez &
            first = True
            for mut in mutacie[strand][1]:
                #print(mut)
                if mut[2].isdigit():
                    num_mut += 1
                    position = int(mut[1:len(mut)-1])-1
                    m1 = barcode_dict[barcode][position][l2n[mut[0]]] #pocet baz zhodnych s referenciou
                    m2 = barcode_dict[barcode][position][l2n[mut[len(mut)-1]]]; #pocet baz zhodnych s mutaciou
                    reads_coverage = barcode_dict[barcode][position][0]+barcode_dict[barcode][position][1]+barcode_dict[barcode][position][2]+barcode_dict[barcode][position][3]
                   
                    if reads_coverage != 0:
                    	probability += m2/reads_coverage 
                    	
                    if m1 < m2 and reads_coverage >= threshold: #ak bolo na danu poziciu namapovanych uz aspon threshold baz a je viac tych zmutovanych                         
                        pocet += 1
                        support.append([mut, m1, m2])
                        if first:
                            mutations_string+=mut
                            first = False
                        else:
                            mutations_string+="&"+mut
            if (pocet > mutacie[strand][0]):
                print(barcode+","+strand+","+str(pocet)+","+mutations_string+","+str(probability/num_mut), file=csv)
    
              
            
def main():
    args = parse_args(sys.argv[1:])   
    reference = list(load_fasta(args.reference))[0][1]
    barcode_dict = load_file(args.file_path, reference)
    mutacie = load_mutations(args.mutations)
    threshold = args.threshold
    with  open(args.output+".csv", "w") as csv:
    	guess(barcode_dict, mutacie, csv, threshold)

    
if __name__ == "__main__":
    main()
