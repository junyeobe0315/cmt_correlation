import pandas as pd
import numpy as np
import scipy
import warnings
from tqdm import tqdm

warnings.filterwarnings('ignore')

def read_data(path):
    data = pd.read_csv(path, low_memory=False)
    pos = data.iloc[:,0]
    name = data.columns.tolist()
    data = data.iloc[:,1:]
    return data, pos, name

def read_10(path):
    data, positions, name = read_data(path)
    name = name[1:]
    df = {}
    pos = []
    for i in tqdm(range(data.shape[0])):
        p = positions[i]
        met = data.iloc[i,:].values.tolist()
        count = 0
        temp_met = []
        for num in met:
            if num == '.':
                pass
            else:
                temp_met.append(num)
                count += 1
        if len(temp_met) == 11:
            df[p] = temp_met
            pos.append(p)
    df = pd.DataFrame(df)
    df = df.T
    df.columns = name
    df.index = pos
    return df, pos

def normality_test(path):
    temp = {}
    data, pos = read_10(path)
    print("Shapiro test 진행")
    for i in tqdm(range(data.shape[0])):
        met = data.iloc[i,:].values.tolist()
        temp_met = list(map(float, met))
        shapiro_test = scipy.stats.shapiro(temp_met)
        met.append(float(shapiro_test.pvalue))
        temp[i] = met
    met_df = pd.DataFrame(temp)
    met_df = met_df.T
    return met_df, pos

def avg_and_std_dev(path):
    _, _, name = read_data(path)
    nor_df, pos = normality_test(path)
    print("평균, 표준편차 구하기 시작")
    avg = []
    std_dev = []
    for i in tqdm(range(nor_df.shape[0])):
        data = nor_df.iloc[i,:].values.tolist()
        if data[-2] == "nan":
            avg.append("nan")
            std_dev.append("nan")
        else:
            temp = []
            for i in range(len(data)-1):
                if data[i] == '.':
                    pass
                else:
                    temp.append(data[i])
            temp = list(map(float, temp))
            avg.append(sum(temp)/len(temp))
            std_dev.append(np.std(temp))
    avg = pd.DataFrame(avg)
    std_dev = pd.DataFrame(std_dev)
    name.extend(["Shapiro p val", "average", "standard dev"])
    name = name[1:]
    df = pd.concat([nor_df, avg, std_dev], axis=1)
    df.columns = name
    df.index = pos
    return df

def concat_(denovo_path, non_denovo_path):
    denovo_df = avg_and_std_dev(denovo_path)
    non_denovo_df = avg_and_std_dev(non_denovo_path)

    d_pos = denovo_df.index.tolist()
    n_pos = non_denovo_df.index.tolist()

    d_name = denovo_df.columns.tolist()
    d_name = d_name[0:11]
    
    n_name = non_denovo_df.columns.tolist()
    n_name = n_name[0:11]

    name = []
    name.extend(d_name)
    name.extend(n_name)
    name.extend(["delta", "t test"])

    temp = {}

    if denovo_df.shape[0] >= non_denovo_df.shape[0]:
        s_df = non_denovo_df.shape[0]
        for i in tqdm(range(s_df)):
            n_p = n_pos[i]
            if n_p in d_pos:
                pos = n_p
                j = d_pos.index(pos)
                d_row = denovo_df.iloc[i,:]
                n_row = non_denovo_df.iloc[j,:]
                d_avg = float(d_row[-2])
                n_avg = float(n_row[-2])
                row = []
                d_met = list(map(float,d_row[0:11]))
                n_met = list(map(float,n_row[0:11]))
                row.extend(d_met)
                row.extend(n_met)
                row.append(d_avg - n_avg)
                levene_test = scipy.stats.levene(d_met, n_met)
                levene = levene_test.pvalue
                if levene > 0.05:
                    p_val = scipy.stats.ttest_ind(d_met, n_met, equal_var=True)
                    t_val = p_val.pvalue
                else:
                    p_val = scipy.stats.ttest_ind(d_met, n_met, equal_var=False)
                    t_val = p_val.pvalue
                row.append(t_val)
                temp[pos] = row
            else:
                pass

    else:
        s_df = denovo_df.shape[0]
        for i in tqdm(range(s_df)):
            d_p = d_pos[i]
            if d_p in n_pos:
                pos = d_p
                j = n_pos.index(pos)
                d_row = denovo_df.iloc[i,:]
                n_row = non_denovo_df.iloc[j,:]
                d_avg = float(d_row[-2])
                n_avg = float(n_row[-2])
                row = []
                d_met = list(map(float,d_row[0:11]))
                n_met = list(map(float,n_row[0:11]))
                row.extend(d_met)
                row.extend(n_met)
                row.append(d_avg - n_avg)
                levene_test = scipy.stats.levene(d_met, n_met)
                levene = levene_test.pvalue
                if levene > 0.05:
                    p_val = scipy.stats.ttest_ind(d_met, n_met, equal_var=True)
                    t_val = p_val.pvalue
                else:
                    p_val = scipy.stats.ttest_ind(d_met, n_met, equal_var=False)
                    t_val = p_val.pvalue
                row.append(t_val)
                temp[pos] = row
            else:
                pass
    df = pd.DataFrame(temp)
    df = df.T
    df.columns = name
    return df

def ttest_to_csv(denovo_path, non_denovo_path, path):
    df = concat_(denovo_path, non_denovo_path)
    df.to_csv(path)
    return 0

def std_dev_to_csv(path_in, path_out):
    df = avg_and_std_dev(path_in)
    df.to_csv(path_out)
    return 0

if __name__ == "__main__":
    denovo_path = "./denovo/dchr22.csv"
    non_denovo_path = "denovo/nchr22.csv"
    df = ttest_to_csv(denovo_path, non_denovo_path, './final_denovo/chr22.csv')
    df = std_dev_to_csv(denovo_path, './final_denovo/dchr22.csv')
    df = std_dev_to_csv(non_denovo_path, './final_denovo/nchr22.csv')
