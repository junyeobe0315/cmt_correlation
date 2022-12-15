import numpy as np # numpy 라는 숫자형 데이터 다루는데 쓰이는 라이브러리 호출
import pandas as pd # pandas 로 엑셀 / csv 불러오기 및 csv 쓰기 데이터 가공
import matplotlib.pyplot as plt # 혹시 모를 데이터 시각화를 위한 툴
import scipy # 여러가지 통계 모델들을 불러와서 사용
import csv # csv 파일을 다루기 위해 라이브러리 사용
import warnings
from tqdm import tqdm

# 엑셀을 불러오고 가공할 수 있는 자료구조로 변경

data = pd.read_csv("./excel_and_csv/Chr5.csv", low_memory=False) # csv 파일 불러오기
patient_name = data.iloc[10, 5:38].to_list()

print(patient_name)
data = data.iloc[11:, 4:38] # 모든 검사자 번호 + 메틸화 정도 추출
print("data shape :", data.shape)


# 정규성을 만족하는지 shapiro test 진행후 데이터에 p-value 추가

normality = list() # p-value 넣을 리스트 생성
new_dataframe = pd.DataFrame()
print("정규성 검사 시작")
for i in tqdm(range(1, data.shape[0])): # 1번 줄부터 마지막 줄까지 정규성 검사를 하기로 선언
    met = data.iloc[i,1:].values.tolist() # 메틸화 정도를 list 에 숫자형으로 집어넣자
    met = list(map(float, met)) # 마찬가지로 확실히 숫자형으로 하기 위한 코드
    shapiro_test = scipy.stats.shapiro(met) # scipy 에서 shapiro test를 가져와서 p value 추출
    met.append(float(shapiro_test.pvalue))
    dataframe_met = pd.DataFrame(met)
    new_dataframe = pd.concat([new_dataframe,dataframe_met], axis=1)
final_data = new_dataframe.T


# 붙여넣어진 p-value 값을 보고 정규성을 만족하는지 확인한 후 환자와 비환자 데이터 나눔
# 정규성을 만족한다면 (p-value > 0.05) 등분산 검정 아니라면 이분산 검정
# 정규성을 만족하지 않는다면 (p-value < 0.05) 윌콕슨 순위합 검정
# 사용한 등분산 검정은 Levene's test 
# t-test 수행시 등분산일 경우 분산이 같다고 가정 이분산일 경우일 경우에 분산이 다르다고 가정


print("patatient number :",len(patient_name))
print("정규성 만족하는 데이터 이분산, 등분산 검정 시작")
new_dataframe = pd.DataFrame(patient_name)
for i in tqdm(range(final_data.shape[0])):
    data = final_data.iloc[i, :].values.tolist()
    if data[-1] > 0.05:
        patient = data[0:21]
        non_patient = data[22:32]
        levene_test = scipy.stats.levene(patient, non_patient)
        data.append(levene_test.pvalue)

        if levene_test.pvalue > 0.05:
            data.append("등분산")
            # 분산이 같다고 가정하고 t test 수행
            t_test = scipy.stats.ttest_ind(patient, non_patient, equal_var=True)
            data.append(t_test.pvalue)
            data = pd.DataFrame(data)
            new_dataframe = pd.concat([new_dataframe, data], axis=1)
        
        else:
            data.append("이분산")
            # 분사이 다르다고 가정하고 웰치스 t test 수행
            t_test = scipy.stats.ttest_ind(patient, non_patient, equal_var=False)
            data.append(t_test.pvalue)
            data = pd.DataFrame(data)
            new_dataframe = pd.concat([new_dataframe, data], axis=1)

    else: # data[-1] < 0.05 -> shapiro test p 값이 0.05 보다 낮은 경우에 대해서
        # 윌콕슨 순위합 검정
        # 일단 좀 나중으로...
        data = pd.DataFrame(data)
        new_dataframe = pd.concat([new_dataframe, data], axis=1)

final_data = new_dataframe.T

with open("final_Chr5.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(final_data.shape[0]):
        row = final_data.iloc[i,:].to_list()
        writer.writerow(row)

