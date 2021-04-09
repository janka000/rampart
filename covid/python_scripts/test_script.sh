#!/bin/sh

mkdir ../annotations/base_count
for file in ../annotations/*.csv
do
  #echo "$(basename "$file"|sed 's/\.[^.]*$//')" >>results.out
  #echo "$(echo "$file"|sed 's/\.[^.]*$//'|sed 's/.*\///')" >> results.out
  python3 ./count_observed_counts.py ../../covid_protocol/references.fasta ../annotations/bam_files/$(basename "$file"|sed 's/\.[^.]*$//').bam ../annotations/$(basename "$file"|sed 's/\.[^.]*$//').csv -o ../annotations/base_count/bases_$(basename "$file"|sed 's/\.[^.]*$//').csv
done

python3 ./merge_dir.py ../annotations/base_count/ ../../covid_protocol/references.fasta ../annotations/base_count/csv.merged

python3 ./compare_mutations.py ../annotations/base_count/csv.merged ../../covid_protocol/references.fasta ./mut.txt -o ../annotations/base_count/compared_mutations
