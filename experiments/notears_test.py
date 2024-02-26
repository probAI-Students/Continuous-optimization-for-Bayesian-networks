from notears.notears.linear import notears_linear
from notears.notears import utils
import os
import pandas as pd

all_files = []

for root, dirs, files in os.walk(r"SKAB/data"):
    for file in files:
        if file.endswith(".csv"):
            all_files.append(os.path.join(root, file))
dfs = []

for path in all_files:
    df = pd.read_csv(path, index_col='datetime', sep=';', parse_dates=True).reset_index(drop=True)
    dfs.append(df)

W_est = notears_linear(dfs[5].values, lambda1=0.1, loss_type='l2')
assert utils.is_dag(W_est)
print(W_est)
