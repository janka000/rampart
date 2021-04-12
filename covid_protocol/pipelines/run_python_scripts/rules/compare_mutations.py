import os
import sys
import argparse
#from collections import defaultdict

from helpers import load_fasta, l2n

letters = "ACGT"

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    parser.add_argument("reference", type=str)
    parser.add_argument("mutations", type=str)
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
                print("found new barcode! "+barcode)
                barcode_dict[barcode] = [[0 for _ in letters] for _ in reference]
            barcode_dict[barcode][position][0]+=A
            barcode_dict[barcode][position][1]+=C
            barcode_dict[barcode][position][2]+=G
            barcode_dict[barcode][position][3]+=T   
    return barcode_dict

def load_mutations(mutations_path):    
    #treba vymysliet nacitanie mut.txt
    
    mut_number = {}
    mutations = {}
    
    with open (mutations_path, "r") as txtfile:
        for line in txtfile:
            line = line.strip()
            if not line.startswith('#') and line:
                columns = line.split(" ")
                mut_number[columns[0]] = columns[1]
                mutations[columns[0]] = []
                mutations[columns[0]].append(int(columns[1]))
                mutations[columns[0]].append([])
                for i in range(2, len(columns)):
                    mutations[columns[0]][1].append(columns[i])
            
    #print(mutations)        
    #return mut_number, mutations #whatever struktura
    return mutations
            
#def print_to_file(nejaky_argument):
#    print(nejaky_agrument, file=f)   
    
def guess(barcode_dict, mutacie, csv, txt):
    #barcode dict - nacitany dictionary zo suboru (pocty ACGT na jednotlivych poziciach v jednotlivych barkodoch)
    #mutacie - nejakym sposobom nacitany subor mut.txt
    #print(barcode_dict)
    print("barcode,strand,support", file=csv)
    for barcode in barcode_dict:
        for nation in mutacie:
            pocet = 0
            support = []
            for mut in mutacie[nation][1]:
                #print(mut)
                if mut[2].isdigit():
                    m1 = barcode_dict[barcode][int(mut[1:len(mut)-1])-1][l2n[mut[0]]]
                    m2 = barcode_dict[barcode][int(mut[1:len(mut)-1])-1][l2n[mut[len(mut)-1]]];
                    if (m1 < m2):
                        #print("mutation "+ nation + ", "+mut+" barkod: "+ barcode +" position in barcode_dict[barcode]: "+str(int(mut[1:len(mut)-1])))
                        pocet += 1
                        support.append([mut, m1, m2])
            if (pocet > mutacie[nation][0]):
                print (barcode + " could be " + nation + " mutation", file=txt)
                print (str(pocet) + " mutations supports it:" + str(support), file=txt)
                #barcode, mutation, support
                print(barcode+","+nation+","+str(pocet), file=csv)
            
    
              
            
def main():
    args = parse_args(sys.argv[1:])   
    reference = list(load_fasta(args.reference))[0][1]
    barcode_dict = load_file(args.file_path, reference)
    #mut_number, mutacie = load_mutations(args.mutations)
    mutacie = load_mutations(args.mutations)
    #nazvi_ma_ako_chces(barcode_dict, mut_number, mutacie)
    with  open(args.output+".csv", "w") as csv:
        with open(args.output+".txt", "w") as txt:
            guess(barcode_dict, mutacie, csv, txt)
    #with open(args.output, "w") as f: #zapis do suboru
    #    print_to_file("test", f)
    
if __name__ == "__main__":
    main()
