import pandas as pd

from monthly_report import load_loans

loans = load_loans()
not_perf = loans[loans["status"] != "Performing"]
largest = loans.loc[loans["principal"].idxmax()]

extra = pd.DataFrame({
    "metric": ["Loans not performing (count)",
               "Principal not performing (GBP)",
               "Largest loan (GBP)", "Largest loan ID"],
    "value": [len(not_perf), round(not_perf["principal"].sum(), 2),
              round(largest["principal"], 2), largest["loan_id"]],
})
print(extra.to_string(index=False))
