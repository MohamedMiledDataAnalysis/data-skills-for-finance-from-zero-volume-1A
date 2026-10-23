# ex2_outliers.py - Exercise 2: IQR outliers by product
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
by_product = loans.groupby("product")["principal"]
q1 = by_product.transform(lambda s: s.quantile(0.25))
q3 = by_product.transform(lambda s: s.quantile(0.75))
loans["lower"] = q1 - 1.5 * (q3 - q1)
loans["upper"] = q3 + 1.5 * (q3 - q1)
loans["outlier"] = ((loans["principal"] > loans["upper"])
                    | (loans["principal"] < loans["lower"]))

summary = loans.groupby("product").agg(
    lower=("lower", "first"),
    upper=("upper", "first"),
    n_out=("outlier", "sum"),
    share_pct=("outlier", "mean"),
)
summary["share_pct"] = 100 * summary["share_pct"]
print(summary.round({"lower": 0, "upper": 0, "share_pct": 1}))

cols = ["loan_id", "product", "principal", "status"]
top = loans[loans["outlier"]].nlargest(5, "principal")
print(top[cols].to_string(index=False))
print(loans["outlier"].sum())
