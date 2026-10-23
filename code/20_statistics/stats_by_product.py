# stats_by_product.py - descriptive statistics for each product
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
loans["p_k"] = loans["principal"] / 1000      # £ thousands
loans["rate_x_p"] = loans["interest_rate"] * loans["principal"]

stats = loans.groupby("product").agg(
    n=("loan_id", "size"),
    mean_k=("p_k", "mean"),
    median_k=("p_k", "median"),
    sd_k=("p_k", "std"),
    p95_k=("p_k", lambda s: s.quantile(0.95)),
    rate_x_p=("rate_x_p", "sum"),
    principal=("principal", "sum"),
)
stats["cv"] = stats["sd_k"] / stats["mean_k"]
stats["rate_w"] = stats["rate_x_p"] / stats["principal"]
stats = stats.drop(columns=["rate_x_p", "principal"])
print(stats.sort_values("mean_k", ascending=False).round(2))
