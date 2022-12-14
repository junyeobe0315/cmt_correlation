import pandas as pd
import dash_bio

df = pd.read_csv("./221129/MW U test.csv", low_memory=False)
dash_bio.ManhattanPlot(
    dataframe=df
)