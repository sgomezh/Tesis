import pandas as pd

data= pd.read_csv("https://users.nber.org/~rdehejia/data/nsw_treated.txt", header = None)

data.to_csv(path_or_buf='control_jobs.csv', index=False)
