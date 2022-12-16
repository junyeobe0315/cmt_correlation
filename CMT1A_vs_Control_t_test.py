import pandas as pd
import scipy
import csv
import warnings
from tqdm import tqdm

warnings.filterwarnings('ignore')
numbers = [str(i) for i in range(1,22)]
numbers.append('X')
numbers.append('Y')
for number in numbers:
    data = pd.read_csv("./cor_data/Chr{}.csv".format(number), low_memory=False)
    patient_name = data.iloc[10, 5:38].to_list()
    pos = data.iloc[11:,4].to_list()
    pos = pd.DataFrame(pos)

    data = data.iloc[11:, 4:38] 
    print("data shape :", data.shape)

    normality = list() 
    new_dataframe = pd.DataFrame()
    print("정규성 검사 시작")
    temp = {}

    for i in tqdm(range(data.shape[0])): 
        met = data.iloc[i,1:].values.tolist()
        met = list(map(float, met)) 
        shapiro_test = scipy.stats.shapiro(met)
        met.append(float(shapiro_test.pvalue))
        temp[i] = met
    dataframe_met = pd.DataFrame(temp)
    final_data = dataframe_met.T
    print("patatient number :",len(patient_name))
    print("이분산, 등분산 검정 시작")
    Levene = []
    Mann = []
    Var = []
    t_vals = []
    for i in tqdm(range(final_data.shape[0])):
        data = final_data.iloc[i, :].values.tolist()
        if data[-1] > 0.05:
            patient = data[0:21]
            non_patient = data[22:32]
            levene_test = scipy.stats.levene(patient, non_patient)
            Levene.append(levene_test.pvalue)
            Mann.append("nan")
            if levene_test.pvalue > 0.05:
                Var.append("등분산")
                # 분산이 같다고 가정하고 t test 수행
                t_test = scipy.stats.ttest_ind(patient, non_patient, equal_var=True)
                t_vals.append(t_test.pvalue)
        
            else:
                Var.append("이분산")
                # 분사이 다르다고 가정하고 웰치스 t test 수행
                t_test = scipy.stats.ttest_ind(patient, non_patient, equal_var=False)
                t_vals.append(t_test.pvalue)

        else: 
            # 윌콕슨 순위합 검정 (Mann-Whitney U 검정)
            patient = data[0:21]
            non_patient = data[22:32]
            mann_test = scipy.stats.mannwhitneyu(patient, non_patient)
            Levene.append("nan")
            Mann.append(mann_test.pvalue)
        
            if mann_test.pvalue > 0.05:
                # equal var
                Var.append("등분산")
                t_test = scipy.stats.ttest_ind(patient, non_patient, equal_var=True)
                t_vals.append(t_test.pvalue)
        
            else:
                # non equal var
                Var.append("이분산")
                t_test = scipy.stats.ttest_ind(patient, non_patient, equal_var=False)
                t_vals.append(t_test.pvalue)

    Levene = pd.DataFrame(Levene)
    Mann = pd.DataFrame(Mann)
    Var = pd.DataFrame(Var)
    t_vals = pd.DataFrame(t_vals)
    new_dataframe = pd.concat([final_data, Levene, Mann, Var, t_vals], axis=1)
    patient_name.extend(["p-val", "Levene test", "Mann-Whitney test", "Varience", "t test"])
    data = new_dataframe.set_axis(patient_name, axis='columns')
    data = data.set_axis(pos, axis="index")

    data.to_csv("./t_test/final_Chr{}.csv".format(number))
