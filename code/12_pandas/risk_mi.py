# risk_mi.py - Applied example: credit risk MI by product
import pandas as pd

pd.options.display.float_format = "{:,.2f}".format

loans = pd.read_csv(
    "data/csv/loans.csv", parse_dates=["origination_date"]
)

loans["in_arrears"] = loans["status"] != "Performing"
loans["arrears_principal"] = loans["principal"].where(
    loans["in_arrears"], 0
)
loans["rate_x_principal"] = (
    loans["interest_rate"] * loans["principal"]
)

mi = loans.groupby("product").agg(
    loans=("loan_id", "count"),
    principal=("principal", "sum"),
    arrears_loans=("in_arrears", "sum"),
    arrears_principal=("arrears_principal", "sum"),
    rate_x_principal=("rate_x_principal", "sum"),
    avg_ltv=("ltv", "mean"),
)
mi["arrears_pct"] = mi["arrears_principal"] / mi["principal"] * 100
mi["wa_rate"] = mi["rate_x_principal"] / mi["principal"]
mi = mi.drop(columns="rate_x_principal")
mi = mi.sort_values("principal", ascending=False)

print(mi[["loans", "principal", "arrears_loans", "arrears_pct"]])
print(mi[["wa_rate", "avg_ltv"]])

mi.round(2).to_csv("output/risk_mi_by_product.csv")
print("Saved output/risk_mi_by_product.csv")
