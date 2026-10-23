# fingerprint.py - a short fingerprint of the loan file
import hashlib

text = open("data/csv/loans.csv").read()
print(hashlib.sha256(text.encode()).hexdigest()[:16])
