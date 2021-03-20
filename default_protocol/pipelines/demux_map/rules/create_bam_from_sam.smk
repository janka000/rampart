rule bam_from_sam:
    input:
        sam =config["output_path"] +"/sam_files/{filename_stem}.sam",
    output:
        bam = config["output_path"]+"/bam_files_from_sam/{filename_stem}.bam"
    threads: 2
    message:
        'creating {output.bam:q} from {input.sam:q} (samtools view -S -b {input.sam:q} > {output.bam:q})'
    shell:
        'samtools view -S -b {input.sam:q} > {output.bam:q}'
        
