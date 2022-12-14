import pysam
import os
from tqdm import tqdm
import pandas as pd

paths =["./raw_data/HN00123650/result_MethylSeq", "./raw_data/HN00139652/HN00139652_result_MethylSeq/result_MethylSeq"]
ignore = [".DS_Store","Analysis_statistics"]
all_data = []
for path in paths:
    file_list = os.listdir(path)
    met_file = list()
    for file in file_list:
        if file not in ignore:
            met_file.append(file)
    
    file_path = [path+"/"+met for met in met_file]
    all_data.extend(file_path)

map_file = []
for path in all_data:
    file_list = os.listdir(path)
    for file in file_list:
        if file[-3:] == "map":
            map_file.append(path+"/"+file)

txt_list = []
for path in map_file:
    file_list = os.listdir(path)
    for file in file_list:
        if file[-3:] == "txt":
            txt_list.append(path+"/"+file)

for txt in tqdm(txt_list):
    len_name = len(txt) - 3
    csv_name = txt[:len_name]+'csv'
    temp = {}
    f = open(txt,'r')
    for line in f:
        if 'chr' in line:
            line_data = line.split('\t')
            temp[line_data[1]] = line_data[4]
    f.close()
    data = pd.DataFrame.from_dict(temp, orient='index')
    data.to_csv(csv_name)
