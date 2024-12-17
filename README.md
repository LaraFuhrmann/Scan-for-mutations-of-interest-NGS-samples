# Scan for mutations of interest in NGS samples processed with V-pipe

Run this workflow on slurm with `run_pipeline.sh`.
To make a dry-run run `snakemake --dry-run`. 

Run workflow and then run notebook to get the heatmap with the frequencies of mutations of interest per sample. 

### Drug resistance mutations
SARS-CoV-2 drug resistance mutations were taken from the Standford Database:  https://covdb.stanford.edu/drms/3clpro/   
They can be formatted in the right way using the notebook: resources/generate_mutations_of_interest_table.ipynb


