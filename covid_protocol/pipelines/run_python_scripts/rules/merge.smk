rule merge:
    input:
    	base_count_folder = config["path"]+"/base_count/",
        ref= config["references_file"]
    output:
        merged_csv = config["path"]+"/base_count/merged.csv",
        csv_merged = config["path"]+"/base_count/csv.merged"
    threads: 3,
    params:
        path_to_script = workflow.current_basedir,
        merged_base_count_path = config["path"]+"/base_count_merged/"
    message:
        "running csv merge script, base_count_folder is {input.base_count_folder:q}"
    shell:
        """ mv {input.base_count_folder:q} {params.merged_base_count_path} &&\
         mkdir -p {input.base_count_folder:q} &&\
         python3 {params.path_to_script}/merge_dir.py {params.merged_base_count_path} {input.ref:q} {output.merged_csv} &&\
         rm -rf {params.merged_base_count_path} &&\
         cp {output.merged_csv} {output.csv_merged} """
