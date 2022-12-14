import pandas as pd


def make_csv(excel_name):
    df = pd.read_excel(excel_name+".xlsx", engine='openpyxl')
    df.to_csv(excel_name+".csv")

if __name__ == '__main__':
    make_csv('ChrX')