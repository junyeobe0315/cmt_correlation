import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm


data = pd.read_csv("high_pval.csv", low_memory=False)
print(data)

for i in tqdm(range(data.shape[0])):
    num = data.iloc[i,0]
    gene = data.iloc[i,2]
    pos = data.iloc[i,4]
    met = data.iloc[i,5:57].values.tolist()
    p_val = data.iloc[i,-1]
    plt.title("gene :{}, pos :{}, p-val :{}".format(gene, pos, p_val))
    stats.probplot(met, dist=stats.norm, plot=plt)
    try:
        plt.savefig("./figure/{}_{}.png".format(gene, pos))
        plt.close()
    except:
        plt.savefig("./figure/number{}.png".format(num))
        plt.close()