# portfolio_summary.py - Applied example: arrears by product
import csv

count = {}         # number of loans per product
principal = {}     # total principal per product
arrears = {}       # number of loans not Performing

with open("data/csv/loans.csv", newline="") as f:
    for row in csv.DictReader(f):
        product = row["product"]
        amount = float(row["principal"])
        count[product] = count.get(product, 0) + 1
        principal[product] = principal.get(product, 0) + amount
        if row["status"] != "Performing":
            arrears[product] = arrears.get(product, 0) + 1

print(f"{'Product':<10}{'Loans':>6}{'Principal (£)':>17}"
      f"{'Arrears':>9}{'Rate':>7}")
for product in sorted(count, key=principal.get, reverse=True):
    n = count[product]
    bad = arrears.get(product, 0)
    print(f"{product:<10}{n:>6}{principal[product]:>17,.2f}"
          f"{bad:>9}{bad / n:>7.1%}")

total_n = sum(count.values())
total_p = sum(principal.values())
total_bad = sum(arrears.values())
print(f"{'Total':<10}{total_n:>6}{total_p:>17,.2f}"
      f"{total_bad:>9}{total_bad / total_n:>7.1%}")

watch = [p for p in count if arrears.get(p, 0) / count[p] > 0.07]
print("Products above the 7% arrears appetite:", watch)
