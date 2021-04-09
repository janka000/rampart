rule minimap2_samtools_bam:
    input:
        fastq=config["input_path"] + "/{filename_stem}.fastq",
        ref= config["references_file"]
    output:
        bam = config["output_path"]+"/bam_files/{filename_stem}.bam",
        bai = config["output_path"]+"/bam_files/{filename_stem}.bam.bai"
    threads: 2
    message:
        "running minimap2 -t 2 -x map-ont -a {input.ref:q} {input.fastq:q} | samtools view -S -b -o - | samtools sort - -o {output.bam:q} && samtools index {output.bam:q}"
    shell:
        "minimap2 -t 2 -x map-ont -a {input.ref:q} {input.fastq:q} | samtools view -S -b -o - | samtools sort - -o {output.bam:q} && samtools index {output.bam:q}"
        
