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

def count_(path):
    data, positions, name = read_data(path)
    name = name[1:]
    name.append("count")
    df = {}
    for i in tqdm(range(data.shape[0])):
        p = positions[i]
        met = data.iloc[i,:].values.tolist()
        count = 0
        temp_met = []
        for num in met:
            if num == '.':
                temp_met.append('.')
            else:
                temp_met.append(num)
                count += 1
        temp_met.append(count)
        df[p] = temp_met
    return df, name

def normality_test(path):
    temp = {}
    data_dict, name = count_(path)
    print("Shapiro test 진행")
    for pos in data_dict:
        met = data_dict[pos]
        count = int(met[-1])
    
        if count == 11:
            temp_met = met[:11]
            temp_met = list(map(float, met))
            shapiro_test = scipy.stats.shapiro(temp_met)
            met.append(float(shapiro_test.pvalue))
        else:
            met.append("nan")

        data_dict[pos] = met
    name.append("shapiro")
    return data_dict, name

def avg_and_std_dev(path):
    data_dict, name = normality_test(path)
    print("평균, 표준편차 구하기 시작")
    for pos in data_dict:
        data = data_dict[pos]
        if int(data[-2]) != 11: # count
            data.append("nan")
            data.append("nan")
        else:
            temp = data[:11]
            temp = list(map(float, temp))
            data.append(sum(temp)/len(temp)) # 평균
            data.append(np.std(temp)) # 표준편차
        data_dict[pos] = data
    name.append("avg")
    name.append("std_dev")
    return data_dict, name

def concat_(denovo_path, non_denovo_path):
    denovo_data, d_name = avg_and_std_dev(denovo_path)
    non_denovo_data, n_name = avg_and_std_dev(non_denovo_path)
    d_pos = [p for p in denovo_data]
    n_pos = [p for p in non_denovo_data]
    
    name = []
    name.extend(d_name)
    name.extend(n_name)

    pos = []
    pos.extend(d_pos)
    pos.extend(n_pos)
    pos = list(set(pos))

    final_data = {}
    for p in pos:
        temp = []
        d_data = denovo_data[p]
        n_data = non_denovo_data[p]
        d_count = d_data[-4]
        n_count = n_data[-4]
        temp.extend(d_data)
        temp.extend(n_data)
        if (int(d_count) == 11 and int(n_count) == 11):
            delta = float(d_data[-2]) - float(n_data[-2])
            d_temp = list(map(float,d_data[:11]))
            n_temp = list(map(float,n_data[:11]))
            levene = scipy.stats.levene(d_temp, n_temp).pvalue
            temp.append(delta)
            temp.append(levene)
        else:
            temp.append("nan")
            temp.append("nan")
        final_data[p] = temp
    name.append("delta")
    name.append("levene t test")
    
    data = pd.DataFrame(final_data)
    data = data.T
    data.columns = name
    return data

def to_csv_(denovo_path, non_denovo_path, path):
    df = concat_(denovo_path, non_denovo_path)
    df.to_csv(path)
    return 0

if __name__ == "__main__":
    denovo = ["./denovo/dchr1.csv","./denovo/dchr2.csv","./denovo/dchr3.csv","./denovo/dchr4.csv","./denovo/dchr5.csv",
                "./denovo/dchr6.csv","./denovo/dchr7.csv","./denovo/dchr8.csv","./denovo/dchr9.csv","./denovo/dchr10.csv",
                "./denovo/dchr11.csv","./denovo/dchr12.csv","./denovo/dchr13.csv","./denovo/dchr14.csv","./denovo/dchr15.csv",
                "./denovo/dchr16.csv","./denovo/dchr17.csv","./denovo/dchr18.csv","./denovo/dchr19.csv","./denovo/dchr20.csv",
                "./denovo/dchr21.csv","./denovo/dchrX.csv","./denovo/dchrY.csv"]

    non_denovo = ["./denovo/nchr1.csv","./denovo/nchr2.csv","./denovo/nchr3.csv","./denovo/nchr4.csv","./denovo/nchr5.csv",
                "./denovo/nchr6.csv","./denovo/nchr7.csv","./denovo/nchr8.csv","./denovo/nchr9.csv","./denovo/nchr10.csv",
                "./denovo/nchr11.csv","./denovo/nchr12.csv","./denovo/nchr13.csv","./denovo/nchr14.csv","./denovo/nchr15.csv",
                "./denovo/nchr16.csv","./denovo/nchr17.csv","./denovo/nchr18.csv","./denovo/nchr19.csv","./denovo/nchr20.csv",
                "./denovo/nchr21.csv","./denovo/nchrX.csv","./denovo/nchrY.csv"]
    test_path_d = "./denovo/dchrY.csv"
    test_path_n = "./denovo/nchrY.csv"

    data = to_csv_(test_path_d, test_path_n, './test.csv')
    print(data)
    exit
    for i in range(len(denovo)):
        denovo_path = denovo[i]
        non_denovo_path = non_denovo[i]
        print(denovo_path)
        print(non_denovo_path)
        df = to_csv_(denovo_path, non_denovo_path, './final_denovo/chr{}.csv'.format(i+1))
        