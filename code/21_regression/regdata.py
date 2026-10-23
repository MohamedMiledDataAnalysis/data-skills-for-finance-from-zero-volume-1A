# regdata.py - load the loans and split them into train and test
import pandas as pd


def load_loans():
    loans = pd.read_csv("data/csv/loans.csv")
    customers = pd.read_csv("data/csv/customers.csv")
    data = loans.merge(
        customers[["customer_id", "risk_rating", "segment"]],
        on="customer_id", how="left")
    assert len(data) == 1200, "The merge changed the row count"
    data["non_performing"] = (
        data["status"] != "Performing").astype(int)
    return data


def split(data):
    number = data["loan_id"].str[1:].astype(int)
    in_test = number % 4 == 0
    return data[~in_test].copy(), data[in_test].copy()


def coef_table(model):
    table = model.params.to_frame("coef")
    table["std_err"] = model.bse
    table["p_value"] = model.pvalues
    ci = model.conf_int()
    table["ci_low"] = ci[0]
    table["ci_high"] = ci[1]
    return table
