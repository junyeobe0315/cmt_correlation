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

def normality_test(path):
    temp = {}
    data, pos, name = read_data(path) 
    print("Shapiro test 진행")
    print("data 3개 이하인 경우 pass")
    for i in tqdm(range(data.shape[0])):
        met = data.iloc[i,:].values.tolist()
        count = 0
        temp_met = []
        for num in met:
            if num == '.':
                pass
            elif float(num) > 1:
                pass
            else:
                temp_met.append(num)
                count += 1
        temp_met = list(map(float, temp_met))
        if len(temp_met) < 3:
            met.append("nan")
        else:
            shapiro_test = scipy.stats.shapiro(temp_met)
            met.append(float(shapiro_test.pvalue))
        met.append(count)
        temp[i] = met
    met_df = pd.DataFrame(temp)
    met_df = met_df.T
    return met_df, pos, name

def avg_and_std_dev(path):
    nor_df, pos, name = normality_test(path)
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
    name.extend(["Shapiro p val", "count","average", "standard dev"])
    name = name[1:]
    df = pd.concat([nor_df, avg, std_dev], axis=1)
    df.columns = name
    df.index = pos
    return df

def concat_t_test(denovo_path, non_denovo_path):
    denovo_df, d_pos, d_name = read_data(denovo_path)
    non_denovo_df, n_pos, n_name = read_data(non_denovo_df)
    assert denovo_df.shape == non_denovo_df.shape
    for i in tqdm(range(len(denovo_df.shape[0]))):
        denovo_met = denovo_df.iloc[i,:].values.tolist()
        non_denovo_met = non_denovo_df.iloc[i,:].values.tolist()
        d_temp = []
        n_temp = []
        d_cnt , n_cnt = 0, 0
        for i in range(len(denovo_met)):
            if denovo_met[i] == '.':
                pass
            else:
                d_temp.append(denovo_met[i])
                d_cnt += 1
            if non_denovo_met[i] == '.':
                pass
            else:
                n_temp.append(non_denovo_met[i])
                n_cnt += 1
            


if __name__ == "__main__":
    path = "./denovo_data/final_denovo/chr21.csv"
    df = avg_and_std_dev(path)
    print(df)
    df.to_csv("test.csv")









