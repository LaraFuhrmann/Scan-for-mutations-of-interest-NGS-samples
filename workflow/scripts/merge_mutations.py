import pandas as pd
from fuc import pyvcf


def main(fnames_snv_csv, fout_all_mutations_csv):

    tmp = []

    for f_snv_vcf in fnames_snv_csv:

        f_snv_vcf = str(f_snv_vcf)

        if f_snv_vcf.endswith(".vcf"):
            df_tmp = pyvcf.VcfFrame.from_file(f_snv_vcf).df
            df_tmp['file'] = f_snv_vcf
        else:
            df_tmp = pd.read_csv(f_snv_vcf)
            df_tmp['file'] = f_snv_vcf

        tmp.append(df_tmp)

    merged_div_csv = pd.concat(
        tmp
    )
    merged_div_csv.to_csv(fout_all_mutations_csv)

if __name__ == "__main__":
    main(
        snakemake.input.fnames_snv_csv,
        snakemake.output.fname_all_mutations,
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
