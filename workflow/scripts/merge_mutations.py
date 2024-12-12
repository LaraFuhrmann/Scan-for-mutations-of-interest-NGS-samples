import pandas as pd
from fuc import pyvcf


def main(fnames_snv_csv, all_samples, fout_all_mutations_csv):

    tmp = []

    for sample, f_snv_vcf in zip(all_samples, fnames_snv_csv):

        f_snv_vcf = str(f_snv_vcf)

        if f_snv_vcf.endswith(".vcf"):
            df_tmp = pyvcf.VcfFrame.from_file(f_snv_vcf).df
            df_tmp['sample'] = sample
        else:
            df_tmp = pd.read_csv(f_snv_vcf)
            df_tmp['sample'] = sample

        tmp.append(df_tmp)

    merged_div_csv = pd.concat(
        tmp
    )
    merged_div_csv.to_csv(fout_all_mutations_csv)

if __name__ == "__main__":
    main(
        snakemake.input.fnames_snv_csv,
        snakemake.params.all_samples,
        snakemake.output.fname_result_csv,
    )


"""
    # filter for positions of interest
    df_muts = df_muts[df_muts['POS'].isin(positions_of_interest)]

    # for samples that don't have positins of interest we need to add an empty lind
    for sample_name in all_samples:
        if sample_name not in df_muts['sample'].unique():
            # create empty row
            df_muts = df_muts.append({'sample':sample_name}, ignore_index=True)
            #df_muts = pd.concat([df_muts, pd.DataFrame({"sample": sample_name})])

"""
