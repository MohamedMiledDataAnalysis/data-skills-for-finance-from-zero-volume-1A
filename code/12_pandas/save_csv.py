# save_csv.py - write a result to the output folder
import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")

arrears = loans.loc[
    loans["status"] != "Performing",
    ["loan_id", "customer_id", "product", "principal", "status"],
].sort_values("principal", ascending=False)

arrears.to_csv("output/arrears_list.csv", index=False)
print(f"Saved {len(arrears)} rows to output/arrears_list.csv")
