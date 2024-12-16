import pandas as pd
from fuc import pyvcf

# variables needed from INFO:
def f_get_DP(row_info):
    return int(row_info.split("DP=")[-1].split(';')[0])

def f_get_n_AltReads(row_info):
    #Number of high-quality ref-forward, ref-reverse, alt-forward and alt-reverse bases
    DP4 = row_info.split("DP4=")[-1].split(';')[0]
    return int(DP4.split(',')[-1]) + int(DP4.split(',')[-2])

def f_get_n_RefReads(row_info):
    #Number of high-quality ref-forward, ref-reverse, alt-forward and alt-reverse bases
    DP4 = row_info.split("DP4=")[-1].split(';')[0]
    return int(DP4.split(',')[0]) + int(DP4.split(',')[1])

def f_get_RefCodon(row_info):
    return row_info.split("RefCodon=")[-1].split(';')[0]

def f_get_AltCodon(row_info):
    return row_info.split("AltCodon=")[-1].split(';')[0]

def f_get_RefAminoAcid(row_info):
    return row_info.split("RefAminoAcid=")[-1].split(';')[0]

def f_get_AltAminoAcid(row_info):
    return row_info.split("AltAminoAcid=")[-1].split(';')[0]

def f_get_CodonPosition(row_info):
    return row_info.split("CodonPosition=")[-1].split(';')[0]

def f_get_SNPCodonPosition(row_info):
    return row_info.split("SNPCodonPosition=")[-1].split(';')[0]

def main(fname_snvs_vcf, fname_mutation_list, fname_snvs_csv):

    tmp = []

    nucleotide_positions_muts_list = pd.read_csv(fname_mutation_list)['PosNucleotide']

    f_snv_vcf = str(f_snv_vcf)
    df_vcf = pyvcf.VcfFrame.from_file(f_snv_vcf).df
    df_vcf['sample'] = f_snv_vcf.split("/")[-4]+"/"+f_snv_vcf.split("/")[-3]
    #df_vcf = df_vcf[df_vcf['POS'].isin(nucleotide_positions_muts_list)]
    if df_vcf.shape[0]==0:
        # add empty row
        df_tmp = pd.DataFrame({"sample": sample_name})
    else:
        df_tmp = df_vcf

    df_tmp['DP'] = df_tmp['INFO'].apply(f_get_DP)
    df_tmp['n_AltReads'] = df_tmp['INFO'].apply(f_get_n_AltReads)
    df_tmp['n_RefReads'] = df_tmp['INFO'].apply(f_get_n_RefReads)
    df_tmp['RefCodon'] = df_tmp['INFO'].apply(f_get_RefCodon)
    df_tmp['AltCodon'] = df_tmp['INFO'].apply(f_get_AltCodon)
    df_tmp['RefAminoAcid'] = df_tmp['INFO'].apply(f_get_RefAminoAcid)
    df_tmp['AltAminoAcid'] = df_tmp['INFO'].apply(f_get_AltAminoAcid)
    df_tmp['CodonPosition'] = df_tmp['INFO'].apply(f_get_CodonPosition)
    df_tmp['SNPCodonPosition'] = df_tmp['INFO'].apply(f_get_SNPCodonPosition)

    df_tmp = df_tmp[['sample','POS', 'REF', 'ALT',  'DP', 'n_AltReads', 'n_RefReads', 'RefCodon', 'AltCodon',
       'RefAminoAcid', 'AltAminoAcid', 'CodonPosition', 'SNPCodonPosition', 'INFO']]

    # load DRM
    df_drm = pd.read_csv(fname_mutation_list)
    df_drm['POS'] = df_drm['PosNucleotide']
    df_drm['CodonPosition'] = df_drm['PosAminoAcid'].astype(int)

    df = pd.merge(df_tmp, df_drm, on=["POS", "AltAminoAcid"], how="inner").to_csv(fname_snvs_csv)

if __name__ == "__main__":
    main(
        snakemake.input.fname_snvs_vcf,
        snakemake.params.fname_mutation_list,
        snakemake.output.fname_snvs_csv,
    )