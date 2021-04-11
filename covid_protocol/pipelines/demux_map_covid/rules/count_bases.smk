rule count_bases:
    input:
        input_csv=config["output_path"] + "/{filename_stem}.csv",
        input_bam=config["output_path"] + "/bam_files/{filename_stem}.bam",
        ref= config["references_file"]
    output:
        csv = config["output_path"]+"/base_count/bc_{filename_stem}.csv"
    params:
        path_to_script = workflow.current_basedir,
    threads: 2
    message:
        "running cout bases script"
    shell:
        """python3 {params.path_to_script}/count_observed_counts.py {input.ref:q} {input.input_bam:q} {input.input_csv:q} -o {output.csv:q}"""
        
