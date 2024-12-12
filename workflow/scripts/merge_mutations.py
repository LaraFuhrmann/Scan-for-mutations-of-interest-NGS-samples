import pandas as pd
from fuc import pyvcf


def main(fnames_snv_csv, fname_mutation_list, all_samples, fout_all_mutations_csv):

    tmp = []

    nucleotide_positions_muts_list = pd.read_csv(fname_mutation_list)['PosNucleotide']

    for sample, f_snv_vcf in zip(all_samples, fnames_snv_csv):

        f_snv_vcf = str(f_snv_vcf)
        df_vcf = pyvcf.VcfFrame.from_file(f_snv_vcf).df
        df_vcf['sample'] = sample
        df_vcf = df_vcf[df_vcf['POS'].isin(nucleotide_positions_muts_list)]
        if df_vcf.shape[0]==0:
            # add empty row
            df_tmp = pd.DataFrame({"sample": sample_name})
        else:
            df_tmp = df_vcf

        tmp.append(df_tmp)

    merged_div_csv = pd.concat(
        tmp
    )

    # weirdly we get nan rows
    #merged_div_csv = merged_div_csv[~merged_div_csv['sample'].isnull()]

    #info_strings = '{"' + merged_div_csv.INFO.str.split(';').str.join('","').str.replace('=','":"').str.replace("\"\",", "") + '"}'
    #info_df = pd.json_normalize(info_strings.apply(eval))
    #merged_div_csv = pd.concat([merged_div_csv, info_df], axis=1)
    merged_div_csv.to_csv(fout_all_mutations_csv)

if __name__ == "__main__":
    main(
        snakemake.input.fnames_snv_csv,
        snakemake.params.fname_mutation_list,
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
