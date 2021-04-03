#!/bin/sh

for file in ../annotations/*.csv
do
  #echo "$(basename "$file"|sed 's/\.[^.]*$//')" >>results.out
  #echo "$(echo "$file"|sed 's/\.[^.]*$//'|sed 's/.*\///')" >> results.out
  python3 ./count_observed_counts.py ../protocols_nanocrop/references.fasta ../annotations/bam_files/$(basename "$file"|sed 's/\.[^.]*$//').bam ../annotations/$(basename "$file"|sed 's/\.[^.]*$//').csv -o ../annotations/base_count/bases_$(basename "$file"|sed 's/\.[^.]*$//').csv
done

