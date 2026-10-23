# five_numbers.py - every measure on five loans, checked by hand
import numpy as np
import pandas as pd

loans_k = pd.Series([12, 15, 18, 25, 80])  # five loans, £ thousands

print(loans_k.mean())
print(loans_k.median())
print(loans_k.max() - loans_k.min())

dev = loans_k - loans_k.mean()             # distance from the mean
print(dev.tolist())
print((dev ** 2).tolist())
print((dev ** 2).sum() / (len(loans_k) - 1))  # variance by hand
print(loans_k.var())
print(loans_k.std())
print(np.std(loans_k))
print(loans_k.quantile([0, 0.25, 0.5, 0.75, 1]))
