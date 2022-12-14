import csv
import pandas as pd

file = pd.read_csv('test.csv')
file.to_excel("test.xlsx")