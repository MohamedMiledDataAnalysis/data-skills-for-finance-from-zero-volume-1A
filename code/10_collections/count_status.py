# count_status.py - count Northbridge loans by status
import csv

counts = {}

with open("data/csv/loans.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        status = row["status"]
        counts[status] = counts.get(status, 0) + 1

print(counts)
total = sum(counts.values())
for status, n in sorted(counts.items()):
    print(f"{status:<12} {n:>5} {n / total:>7.1%}")
print(f"{'Total':<12} {total:>5}")
