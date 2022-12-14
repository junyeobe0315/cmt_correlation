import matplotlib.pyplot as plt
import csv
import pandas as pd
from tqdm import tqdm

def read_data(FILE_NAME):
    data = pd.read_csv("./final_cor/correlation_{}.csv".format(FILE_NAME), low_memory=False)
    cmtns = list(map(float, data.loc[0,"FC272-7":"FC1127-3"].values.tolist()))
    high_r_val_id = []
    error_lst = []
    for i in tqdm(range(1, data.shape[0])):
        test = data.loc[i, "test_name"]
        if test == "Pearson test":
            r_val = data.loc[i, "Pearson_r"]
        if test == "Spearman test":
            r_val = data.loc[i, "Spearman_r"]
        
        if abs(r_val) > 1:
            error_lst.append(i)
        if abs(r_val) > 0.7:
            high_r_val_id.append(i)

    final_id = [x for x in high_r_val_id if x not in error_lst]

    return final_id, data, cmtns

def draw_scatter_plot(FILE_NAME):
    final_id, data, cmtns = read_data(FILE_NAME)
    for idx in final_id:
        met_lev = list(map(float, data.iloc[idx, 1:23].values))
        pos = data.iloc[idx, 0]
        test = data.iloc[idx, 24]

        if test == "Pearson test":
            r_val = data.loc[idx, "Pearson_r"]
        if test == "Spearman test":
            r_val = data.loc[idx, "Spearman_r"]

        plt.title("{} / pos : {} / r value :{}".format(FILE_NAME, pos, r_val))
        plt.xlabel("CMTNS")
        plt.ylim([0,1])
        plt.ylabel("Met level")
        plt.scatter(cmtns, met_lev)
        plt.show()

if __name__ == "__main__":
    FILE_NAMES = ["Chr1", "Chr2", "Chr3",
                    "Chr4", "Chr5", "Chr6",
                    "Chr7", "Chr8", "Chr9",
                    "Chr10", "Chr11", "Chr12",
                    "Chr13", "Chr14", "Chr15",
                    "Chr16", "Chr17", "Chr18",
                    "Chr19", "Chr20", "Chr21",
                    "Chr22", "ChrX", "ChrY",]
    for FILE_NAME in FILE_NAMES:
        draw_scatter_plot(FILE_NAME)