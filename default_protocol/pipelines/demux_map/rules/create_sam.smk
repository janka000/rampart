rule minimap2_sam:
    input:
        fastq=config["input_path"] + "/{filename_stem}.fastq",
        ref= config["references_file"]
    output:
        sam = config["output_path"]+"/sam_files/{filename_stem}.sam"
    threads: 2
    message:
        "running minimap2 -t 2 -x map-ont -a {input.ref:q} {input.fastq:q} > {output.sam:q}"
    shell:
        'minimap2 -t 2 -x map-ont -a {input.ref:q} {input.fastq:q} > {output.sam:q}'
        
