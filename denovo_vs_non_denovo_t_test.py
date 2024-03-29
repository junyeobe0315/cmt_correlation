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
    name = name[1:11] # 11 지우면 16년도 데이터 지원
    name.append("count")
    df = {}
    for i in tqdm(range(data.shape[0])):
        p = positions[i]
        met = data.iloc[i,:10].values.tolist() # 10 지우면 16년도 데이터 지원
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
    data_dict, name = count_(path)
    print("Shapiro test 진행")
    for pos in data_dict:
        met = data_dict[pos]
        count = int(met[-1])
        if count == 10:
            temp_met = met[:10]
            temp_met = list(map(float, temp_met))
            shapiro_test = scipy.stats.shapiro(temp_met)
            met.append(shapiro_test.pvalue)
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
        if int(data[-2]) != 10: # count
            data.append("nan")
            data.append("nan")
        else:
            temp = data[:10]
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
        if (int(d_count) == 10 and int(n_count) == 10): # == 10 이면 16년도 데이터 제외함
            delta = float(d_data[-2]) - float(n_data[-2])
            d_temp = list(map(float,d_data[:10]))
            n_temp = list(map(float,n_data[:10]))
            levene = scipy.stats.levene(d_temp, n_temp).pvalue
            if levene < 0.05:
                t_test = scipy.stats.ttest_ind(d_temp, n_temp, equal_var=False).pvalue
            else:
                t_test = scipy.stats.ttest_ind(d_temp, n_temp, equal_var=True).pvalue
            temp.append(delta)
            temp.append(levene)
            temp.append(t_test)
        else:
            temp.append("nan")
            temp.append("nan")
            temp.append("nan")
        final_data[p] = temp
    name.append("delta")
    name.append("levene test")
    name.append("t test p value")
    
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
                "./denovo/dchr21.csv","./denovo/dchr22.csv"]

    non_denovo = ["./denovo/nchr1.csv","./denovo/nchr2.csv","./denovo/nchr3.csv","./denovo/nchr4.csv","./denovo/nchr5.csv",
                "./denovo/nchr6.csv","./denovo/nchr7.csv","./denovo/nchr8.csv","./denovo/nchr9.csv","./denovo/nchr10.csv",
                "./denovo/nchr11.csv","./denovo/nchr12.csv","./denovo/nchr13.csv","./denovo/nchr14.csv","./denovo/nchr15.csv",
                "./denovo/nchr16.csv","./denovo/nchr17.csv","./denovo/nchr18.csv","./denovo/nchr19.csv","./denovo/nchr20.csv",
                "./denovo/nchr21.csv","./denovo/nchr22.csv"]
    
    
    for i in range(len(denovo)):
        denovo_path = denovo[i]
        non_denovo_path = non_denovo[i]
        print(denovo_path)
        print(non_denovo_path)
        df = to_csv_(denovo_path, non_denovo_path, './final_denovo/chr{}.csv'.format(i+1))
    
    denovo_x = "./denovo/dchrX.csv"
    non_denovo_x = "./denovo/nchrX.csv"
    df = to_csv_(denovo_x, non_denovo_x, "./final_denovo/chrX.csv")

    denovo_y = "./denovo/dchrY.csv"
    non_denovo_y = "./denovo/nchrY.csv"
    df = to_csv_(denovo_y, non_denovo_y, "./final_denovo/chrY.csv")
    