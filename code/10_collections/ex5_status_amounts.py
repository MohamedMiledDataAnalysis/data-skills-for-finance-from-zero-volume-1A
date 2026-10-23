# ex5_status_amounts.py - Exercise 5: principal by status
import csv

amount = {}
largest = {}

with open("data/csv/loans.csv", newline="") as f:
    for row in csv.DictReader(f):
        status = row["status"]
        p = float(row["principal"])
        amount[status] = amount.get(status, 0) + p
        if p > largest.get(status, (0, ""))[0]:
            largest[status] = (p, row["loan_id"])

order = ["Performing", "30+ DPD", "90+ DPD", "Default"]
total = sum(amount.values())
for status in order:
    p, loan_id = largest[status]
    print(f"{status:<11} £{amount[status]:>15,.2f} "
          f"{amount[status] / total:>6.1%}  largest {loan_id}"
          f" £{p:,.2f}")
