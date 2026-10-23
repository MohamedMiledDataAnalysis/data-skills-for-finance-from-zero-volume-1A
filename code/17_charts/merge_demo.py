import pandas as pd

loans = pd.read_csv("data/csv/loans.csv")
customers = pd.read_csv("data/csv/customers.csv")
ratings = customers[["customer_id", "risk_rating"]]
print("Loans:", len(loans), "| customers:", len(ratings))

data = loans.merge(ratings, on="customer_id", how="left")
print("After left merge:", len(data), "rows")
print(data[["loan_id", "customer_id", "risk_rating"]].head(3))

private = customers.loc[customers["segment"] == "Private",
                        ["customer_id", "segment"]]
left = loans.merge(private, on="customer_id", how="left")
inner = loans.merge(private, on="customer_id", how="inner")
print("Left with Private only: ", len(left), "rows,",
      left["segment"].isna().sum(), "without a segment")
print("Inner with Private only:", len(inner), "rows")
