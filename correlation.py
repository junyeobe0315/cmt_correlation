import pandas as pd
import scipy.stats as stats
import csv
from tqdm import tqdm
import numpy as np
import warnings

def make_dict():
    
    data = pd.read_csv("./cor_data.csv")
    patient_dict = {}
    cmtns_list = []
    for i in range(data.shape[1]):
        key = data.iloc[0,i]
        cmt_lev = data.iloc[1,i]
        patient_dict[key] = []
        cmtns_list.append(cmt_lev)
    cmtns_list = list(map(float,cmtns_list))

    return patient_dict, cmtns_list

def make_df(FILE_NAME):
    
    data = pd.read_csv("./cor_data/{}.csv".format(FILE_NAME), low_memory=False)
    # make position list
    # Pos row, col data.iloc[10, 4]
    pos_list = data.iloc[11:, 4].to_list()
    
    # add met level to patient_dict
    # make dict {patient name : met level index}
    patient_dict, cmtns_list = make_dict()
    file_patient_list = data.iloc[10,5:].to_list()
    file_patient_pos = {}
    for idx, patient in enumerate(file_patient_list):
        file_patient_pos[patient] = idx+5
    
    # let's add met level to patient_dict
    for key in patient_dict:
        if key in file_patient_list:
            idx = file_patient_pos[key]
            met_lev = data.iloc[11:, idx].to_list()
            patient_dict[key].extend(met_lev)

    # index = pos_list 
    met_df = pd.DataFrame(data=patient_dict, index=pos_list)

    return met_df

def correlation_test(data):
    # call cmtns list
    patient_dict, cmtns_list = make_dict()
    
    # make dict to save p value / test name / r value
    # need to make dataframe after adding data
    concat_dict = {"Shapiro_test" : [], "test_name" : [], "Pearson_r" : [], "Spearman_r" : [], "test p-val": []}

    # let's make code that reads lines
    # read line -> shapiro test
    # if shapiro test p val > 0.05:
    #   pearson test
    # elif shapiro test p val < 0.05:
    #   spearman test
    for i in tqdm(range(data.shape[0])):
        met_level = data.iloc[i,:].to_list()
        met_level = list(map(float, met_level))
        shapiro_test = stats.shapiro(met_level)
        p_val = float(shapiro_test.pvalue)
        concat_dict["Shapiro_test"].append(p_val)
        if p_val > 0.05:
            concat_dict["test_name"].append("Pearson test")
            res = stats.pearsonr(cmtns_list, met_level)
            r = res.statistic
            p = res.pvalue
            concat_dict["Pearson_r"].append(r)
            concat_dict["Spearman_r"].append("nan")
            concat_dict["test p-val"].append(p)
        else:
            concat_dict["test_name"].append("Spearman test")
            res = stats.spearmanr(cmtns_list, met_level)
            r = res.correlation
            p = res.pvalue
            concat_dict["Pearson_r"].append("nan")
            concat_dict["Spearman_r"].append(r)
            concat_dict["test p-val"].append(p)

    # let's concat dict to data
    # get index from data
    # dict -> dataframe with index -> concat
    index_list = data.index
    concat_df = pd.DataFrame(data=concat_dict, index=index_list)
    final_df = pd.concat([data, concat_df], axis=1)

    return final_df

def concat_cmtns(final_data):
    # read data from cor data csv
    # make patient_dict = {patient : cmtns}
    patient_data = pd.read_csv("./cor_data.csv")
    patient_dict = {}
    for i in range(patient_data.shape[1]):
        key = patient_data.iloc[0,i]
        cmtns = patient_data.iloc[1,i]
        patient_dict[key] = float(cmtns)
    
    # make patient_dict { ... , shapiro test : nan, test name : nan, pearson_r : nan, spearman_r : nan}
    patient_dict["Shapiro_test"] = "nan"
    patient_dict["test_name"] = "nan"
    patient_dict["Pearson_r"] = "nan"
    patient_dict["Spearman_r"] = "nan"
    patient_dict["test p-val"] = "nan"
    # make patient_dict -> dataframe
    # concat with final_data
    patient_df = pd.DataFrame(data=patient_dict, index=["CMTNS"])
    final_data = pd.concat([patient_df, final_data], ignore_index=False)

    return final_data

def make_csv(FILE_NAME):
    met_df = make_df(FILE_NAME)
    final_df = correlation_test(met_df)
    final_data = concat_cmtns(final_df)
    final_data.to_csv("./final_cor/correlation_{}.csv".format(FILE_NAME))
    return final_data    

if __name__ == "__main__":
    warnings.filterwarnings(action='ignore')
    FILE_NAMES= ["Chr18", "Chr19", "Chr20", "Chr21", "Chr22", "ChrX", "ChrY"]
    print("make sure that all lib are loaded")
    for FILE_NAME in FILE_NAMES:
        final_data = make_csv(FILE_NAME)
