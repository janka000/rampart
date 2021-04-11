rule count_and_compare:
    input:
        mut= config["mutations_file"],
        ref= config["references_file"],
        merged_file=config["path"]+"/base_count/csv.merged"
    output:
        csv = config["path"]+"/results/mutations.csv"
    threads: 2,
    params:
        path_to_script = workflow.current_basedir,
        out_dir = config["path"]+"/results",
        output = config["path"]+"/results/mutations"
    message:
        "running count and compare script"
    shell:
        """
        mkdir -p {params.out_dir} &&\
        python3 {params.path_to_script}/compare_mutations.py {input.merged_file:q} {input.ref:q} {input.mut:q} -o {params.output} &&\
        rm {input.merged_file:q} """
        
