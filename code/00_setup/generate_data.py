"""
generate_data.py — builds the Northbridge Bank dataset used in every chapter.

Northbridge Bank is a fictional UK bank. Every number in this dataset is
synthetic. The random seed is fixed, so every reader who runs this script
gets exactly the same files, row for row.

Run it once from the book's companion folder:

    python code/00_setup/generate_data.py

It writes:
    data/csv/       customers.csv, accounts.csv, transactions.csv,
                    loans.csv, fx_rates.csv, market_prices.csv
    data/excel/     northbridge.xlsx   (one sheet per table)
    data/json/      loans.json, customers.json
    data/sql/       northbridge_sqlserver.sql  (T-SQL script for SQL Server)
    data/loan_tape/ loan_tape.csv, loan_tape_control.csv  (Chapter 19)
    data/northbridge.db                (SQLite copy, used by the test harness)
"""

import json
import math
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

SEED = 2026
random.seed(SEED)

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
for sub in ["csv", "excel", "json", "sql"]:
    (DATA / sub).mkdir(parents=True, exist_ok=True)
(ROOT / "output").mkdir(exist_ok=True)   # where every chapter saves results

FIRST = ["Olivia", "Amelia", "Isla", "Ava", "Mia", "Sophia", "Grace", "Lily",
         "Freya", "Emily", "Oliver", "George", "Noah", "Arthur", "Leo", "Harry",
         "Oscar", "Jack", "Charlie", "Thomas", "Amira", "Yusuf", "Priya", "Arjun",
         "Chloe", "Lucas", "Camille", "Hugo", "Sofia", "Mateo"]
LAST = ["Smith", "Jones", "Taylor", "Brown", "Williams", "Wilson", "Johnson",
        "Davies", "Patel", "Robinson", "Wright", "Thompson", "Evans", "Walker",
        "White", "Roberts", "Green", "Hall", "Khan", "Clarke", "Martin", "Bernard",
        "Dubois", "Moreau", "Garcia", "Rossi", "Muller", "Novak", "Ahmed", "Lewis"]
CITIES = [("London", "United Kingdom", 0.30), ("Manchester", "United Kingdom", 0.12),
          ("Birmingham", "United Kingdom", 0.10), ("Edinburgh", "United Kingdom", 0.08),
          ("Bristol", "United Kingdom", 0.07), ("Leeds", "United Kingdom", 0.07),
          ("Paris", "France", 0.10), ("Lyon", "France", 0.04),
          ("Frankfurt", "Germany", 0.06), ("New York", "United States", 0.06)]
SEGMENTS = [("Retail", 0.70), ("Private", 0.10), ("SME", 0.20)]


def weighted(choices):
    r = random.random()
    acc = 0.0
    for *value, w in choices:
        acc += w
        if r <= acc:
            return value[0] if len(value) == 1 else tuple(value)
    last = choices[-1]
    return last[0] if len(last) == 2 else tuple(last[:-1])


def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


# ---------------------------------------------------------------- customers
customers = []
for i in range(1, 501):
    city, country = weighted(CITIES)
    customers.append({
        "customer_id": f"C{i:04d}",
        "first_name": random.choice(FIRST),
        "last_name": random.choice(LAST),
        "city": city,
        "country": country,
        "segment": weighted(SEGMENTS),
        "join_date": rand_date(date(2012, 1, 1), date(2024, 12, 31)).isoformat(),
        "risk_rating": random.choices([1, 2, 3, 4, 5], [10, 30, 35, 18, 7])[0],
    })
cust_df = pd.DataFrame(customers)

# ---------------------------------------------------------------- accounts
CCY_BY_COUNTRY = {"United Kingdom": "GBP", "France": "EUR", "Germany": "EUR",
                  "United States": "USD"}
accounts = []
a = 1
for c in customers:
    n = random.choices([1, 2, 3], [45, 40, 15])[0]
    types = random.sample(["Current", "Savings", "Investment"], n)
    if "Current" not in types:
        types[0] = "Current"
    for t in types:
        base = {"Current": 2500, "Savings": 15000, "Investment": 60000}[t]
        if c["segment"] == "Private":
            base *= 8
        elif c["segment"] == "SME":
            base *= 3
        balance = round(random.lognormvariate(math.log(base), 0.9), 2)
        if t == "Current" and random.random() < 0.06:
            balance = -round(random.uniform(50, 1500), 2)  # overdrawn
        open_d = max(date.fromisoformat(c["join_date"]),
                     rand_date(date(2012, 1, 1), date(2025, 6, 30)))
        accounts.append({
            "account_id": f"A{a:05d}",
            "customer_id": c["customer_id"],
            "account_type": t,
            "currency": CCY_BY_COUNTRY[c["country"]],
            "open_date": open_d.isoformat(),
            "balance": balance,
        })
        a += 1
acc_df = pd.DataFrame(accounts)

# ---------------------------------------------------------------- fx rates
# Business days of 2025; units of the currency per 1 GBP.
fx = []
d = date(2025, 1, 1)
eur, usd = 1.20, 1.25
while d <= date(2025, 12, 31):
    if d.weekday() < 5:
        eur *= math.exp(random.gauss(0, 0.0035))
        usd *= math.exp(random.gauss(0.00005, 0.0045))
        fx.append({"rate_date": d.isoformat(), "currency": "EUR", "rate_per_gbp": round(eur, 4)})
        fx.append({"rate_date": d.isoformat(), "currency": "USD", "rate_per_gbp": round(usd, 4)})
    d += timedelta(days=1)
fx_df = pd.DataFrame(fx)

# ---------------------------------------------------------------- transactions
CATS = [("Salary", 0.08), ("Groceries", 0.20), ("Rent", 0.06), ("Utilities", 0.08),
        ("Travel", 0.08), ("Restaurants", 0.14), ("Shopping", 0.16),
        ("Transfer", 0.12), ("Fees", 0.03), ("Interest", 0.05)]
AMT = {"Salary": (3200, 0.35, 1), "Groceries": (65, 0.6, -1), "Rent": (1300, 0.3, -1),
       "Utilities": (120, 0.4, -1), "Travel": (240, 0.9, -1), "Restaurants": (45, 0.6, -1),
       "Shopping": (90, 0.9, -1), "Transfer": (400, 1.0, 0), "Fees": (12, 0.5, -1),
       "Interest": (25, 1.0, 1)}
CHANNELS = [("Card", 0.55), ("Online", 0.25), ("Mobile", 0.15), ("Branch", 0.05)]
txns = []
active = [x for x in accounts if x["account_type"] in ("Current", "Savings")]
for t in range(1, 20001):
    acct = random.choice(active)
    cat = weighted(CATS)
    if acct["account_type"] == "Savings":
        cat = random.choice(["Transfer", "Interest"])
    mu, sigma, sign = AMT[cat]
    amount = round(random.lognormvariate(math.log(mu), sigma), 2)
    if sign == 0:
        sign = random.choice([-1, 1])
    txns.append({
        "transaction_id": f"T{t:06d}",
        "account_id": acct["account_id"],
        "txn_date": rand_date(date(2025, 1, 1), date(2025, 12, 31)).isoformat(),
        "amount": sign * amount,
        "currency": acct["currency"],
        "category": cat,
        "channel": "Online" if cat in ("Salary", "Interest") else weighted(CHANNELS),
    })
txn_df = pd.DataFrame(txns).sort_values(["txn_date", "transaction_id"]).reset_index(drop=True)

# ---------------------------------------------------------------- loans
PRODUCTS = [("Mortgage", 0.40), ("Personal", 0.30), ("Auto", 0.18), ("SME", 0.12)]
loans = []
for i in range(1, 1201):
    c = random.choice(customers)
    prod = weighted(PRODUCTS)
    if c["segment"] == "SME" and random.random() < 0.6:
        prod = "SME"
    principal = {"Mortgage": random.lognormvariate(math.log(240000), 0.45),
                 "Personal": random.lognormvariate(math.log(12000), 0.55),
                 "Auto": random.lognormvariate(math.log(22000), 0.4),
                 "SME": random.lognormvariate(math.log(150000), 0.7)}[prod]
    term = {"Mortgage": random.choice([240, 300, 360]), "Personal": random.choice([24, 36, 48, 60]),
            "Auto": random.choice([36, 48, 60]), "SME": random.choice([36, 60, 84, 120])}[prod]
    base_rate = {"Mortgage": 4.2, "Personal": 7.5, "Auto": 6.4, "SME": 6.9}[prod]
    rate = round(base_rate + 0.45 * (c["risk_rating"] - 3) + random.gauss(0, 0.35), 2)
    pd_ = 0.015 * c["risk_rating"] ** 1.6
    r = random.random()
    if r < pd_ * 0.35:
        status = "Default"
    elif r < pd_ * 0.6:
        status = "90+ DPD"
    elif r < pd_:
        status = "30+ DPD"
    else:
        status = "Performing"
    ltv = round(random.uniform(45, 95), 1) if prod == "Mortgage" else None
    loans.append({
        "loan_id": f"L{i:05d}",
        "customer_id": c["customer_id"],
        "product": prod,
        "principal": round(principal, 2),
        "interest_rate": rate,
        "term_months": term,
        "origination_date": rand_date(date(2018, 1, 1), date(2025, 9, 30)).isoformat(),
        "status": status,
        "ltv": ltv,
    })
loan_df = pd.DataFrame(loans)

# ---------------------------------------------------------------- market prices
TICKERS = {"NBB": (14.20, 0.0002, 0.016), "ATLS": (102.50, 0.0004, 0.012),
           "GRNE": (48.00, 0.0006, 0.022), "MERC": (230.00, 0.0001, 0.009)}
prices = []
levels = {k: v[0] for k, v in TICKERS.items()}
d = date(2025, 1, 1)
while d <= date(2025, 12, 31):
    if d.weekday() < 5:
        for tk, (_, drift, vol) in TICKERS.items():
            levels[tk] *= math.exp(drift + random.gauss(0, vol))
            prices.append({"price_date": d.isoformat(), "ticker": tk,
                           "close": round(levels[tk], 2),
                           "volume": int(random.lognormvariate(math.log(250000), 0.4))})
    d += timedelta(days=1)
px_df = pd.DataFrame(prices)

TABLES = {"customers": cust_df, "accounts": acc_df, "transactions": txn_df,
          "loans": loan_df, "fx_rates": fx_df, "market_prices": px_df}

# ---------------------------------------------------------------- write files
for name, df in TABLES.items():
    df.to_csv(DATA / "csv" / f"{name}.csv", index=False, lineterminator="\n")

with pd.ExcelWriter(DATA / "excel" / "northbridge.xlsx") as xw:
    for name, df in TABLES.items():
        if name != "transactions":           # keep the workbook small
            df.to_excel(xw, sheet_name=name, index=False)
    txn_df.head(2000).to_excel(xw, sheet_name="transactions_sample", index=False)

loan_records = [{k: (None if isinstance(v, float) and math.isnan(v) else v)
                 for k, v in row.items()}
                for row in loan_df.to_dict(orient="records")]
(DATA / "json" / "loans.json").write_text(
    json.dumps(loan_records, indent=2, allow_nan=False), newline="\n")
# A nested JSON file: each customer with the list of their accounts.
nested = []
for c in customers:
    nested.append({**{k: c[k] for k in ("customer_id", "first_name", "last_name", "segment")},
                   "address": {"city": c["city"], "country": c["country"]},
                   "accounts": [{k: x[k] for k in ("account_id", "account_type", "currency", "balance")}
                                for x in accounts if x["customer_id"] == c["customer_id"]]})
(DATA / "json" / "customers.json").write_text(json.dumps(nested, indent=2), newline="\n")

# ---------------------------------------------------------------- SQLite copy
db = DATA / "northbridge.db"
if db.exists():
    db.unlink()
with sqlite3.connect(db) as con:
    for name, df in TABLES.items():
        df.to_sql(name, con, index=False)

# ---------------------------------------------------------------- SQL Server script
DDL = """
CREATE TABLE dbo.customers (
    customer_id   VARCHAR(10)  NOT NULL PRIMARY KEY,
    first_name    NVARCHAR(50) NOT NULL,
    last_name     NVARCHAR(50) NOT NULL,
    city          NVARCHAR(50) NOT NULL,
    country       NVARCHAR(50) NOT NULL,
    segment       VARCHAR(10)  NOT NULL,
    join_date     DATE         NOT NULL,
    risk_rating   TINYINT      NOT NULL
);
CREATE TABLE dbo.accounts (
    account_id    VARCHAR(10)   NOT NULL PRIMARY KEY,
    customer_id   VARCHAR(10)   NOT NULL REFERENCES dbo.customers(customer_id),
    account_type  VARCHAR(12)   NOT NULL,
    currency      CHAR(3)       NOT NULL,
    open_date     DATE          NOT NULL,
    balance       DECIMAL(14,2) NOT NULL
);
CREATE TABLE dbo.transactions (
    transaction_id VARCHAR(10)   NOT NULL PRIMARY KEY,
    account_id     VARCHAR(10)   NOT NULL REFERENCES dbo.accounts(account_id),
    txn_date       DATE          NOT NULL,
    amount         DECIMAL(14,2) NOT NULL,
    currency       CHAR(3)       NOT NULL,
    category       VARCHAR(20)   NOT NULL,
    channel        VARCHAR(10)   NOT NULL
);
CREATE TABLE dbo.loans (
    loan_id          VARCHAR(10)   NOT NULL PRIMARY KEY,
    customer_id      VARCHAR(10)   NOT NULL REFERENCES dbo.customers(customer_id),
    product          VARCHAR(10)   NOT NULL,
    principal        DECIMAL(14,2) NOT NULL,
    interest_rate    DECIMAL(5,2)  NOT NULL,
    term_months      SMALLINT      NOT NULL,
    origination_date DATE          NOT NULL,
    status           VARCHAR(12)   NOT NULL,
    ltv              DECIMAL(5,1)  NULL
);
CREATE TABLE dbo.fx_rates (
    rate_date     DATE         NOT NULL,
    currency      CHAR(3)      NOT NULL,
    rate_per_gbp  DECIMAL(9,4) NOT NULL,
    PRIMARY KEY (rate_date, currency)
);
CREATE TABLE dbo.market_prices (
    price_date  DATE          NOT NULL,
    ticker      VARCHAR(6)    NOT NULL,
    [close]     DECIMAL(10,2) NOT NULL,
    volume      INT           NOT NULL,
    PRIMARY KEY (price_date, ticker)
);
GO
"""


def sql_value(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "NULL"
    if isinstance(v, str):
        return "N'" + v.replace("'", "''") + "'"
    return repr(v) if isinstance(v, float) else str(v)


lines = ["-- Northbridge Bank sample database for Microsoft SQL Server",
         "-- Generated by generate_data.py (seed 2026). Synthetic data only.",
         "IF DB_ID('Northbridge') IS NULL CREATE DATABASE Northbridge;",
         "GO", "USE Northbridge;", "GO",
         "DROP TABLE IF EXISTS dbo.transactions, dbo.loans, dbo.accounts, "
         "dbo.customers, dbo.fx_rates, dbo.market_prices;", "GO", DDL,
         "SET NOCOUNT ON;"]
for name in ["customers", "accounts", "transactions", "loans", "fx_rates", "market_prices"]:
    df = TABLES[name]
    cols = ", ".join("[close]" if c == "close" else c for c in df.columns)
    rows = df.astype(object).where(df.notna(), None).values.tolist()
    for start in range(0, len(rows), 1000):        # SQL Server allows 1,000 rows per VALUES
        chunk = rows[start:start + 1000]
        lines.append(f"INSERT INTO dbo.{name} ({cols}) VALUES")
        lines.append(",\n".join("(" + ", ".join(sql_value(v) for v in r) + ")" for r in chunk) + ";")
    lines.append("GO")
lines.append("SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM dbo.customers UNION ALL "
             "SELECT 'accounts', COUNT(*) FROM dbo.accounts UNION ALL "
             "SELECT 'transactions', COUNT(*) FROM dbo.transactions UNION ALL "
             "SELECT 'loans', COUNT(*) FROM dbo.loans UNION ALL "
             "SELECT 'fx_rates', COUNT(*) FROM dbo.fx_rates UNION ALL "
             "SELECT 'market_prices', COUNT(*) FROM dbo.market_prices;")
(DATA / "sql" / "northbridge_sqlserver.sql").write_text("\n".join(lines), encoding="utf-8", newline="\n")

# ---------------------------------------------------------------- loan tape
# A residential mortgage loan tape, as a bank sends it to investors and
# rating agencies when it securitises a pool: one row per loan at the
# cut-off date 31 December 2025, 25 standard fields. Chapter 19 checks it.
#
# The tape deliberately contains the defects real tapes contain, so that
# the data-quality checks have something to find. Planted defects:
#   uniqueness    3 exact duplicate rows; 2 loan_id reused by another loan
#   completeness  12 blank property_value; 5 blank interest_rate;
#                 4 blank region
#   validity      4 interest_rate keyed in basis points (425 = 4.25%);
#                 3 status "PERF" (legacy code); 3 negative current_balance;
#                 5 property_value keyed in thousands (LTV > 150%);
#                 2 origination_date after the cut-off date
#   consistency   4 maturity_date before origination_date;
#                 6 current_balance above original_balance;
#                 7 status "Current" with days_in_arrears >= 30;
#                 3 current_ltv that does not match balance / value
#   format        5 origination_date written as DD/MM/YYYY
# The control-totals file holds the servicer's figures for the clean pool.
rt = random.Random(SEED + 16)
CUTOFF = date(2025, 12, 31)
REGIONS = [("London", 0.16), ("South East", 0.18), ("South West", 0.09),
           ("East of England", 0.10), ("West Midlands", 0.08),
           ("East Midlands", 0.07), ("North West", 0.11),
           ("Yorkshire and the Humber", 0.08), ("North East", 0.04),
           ("Wales", 0.04), ("Scotland", 0.05)]
REGION_PRICE = {"London": 520000, "South East": 390000, "South West": 320000,
                "East of England": 340000, "West Midlands": 245000,
                "East Midlands": 235000, "North West": 210000,
                "Yorkshire and the Humber": 200000, "North East": 160000,
                "Wales": 205000, "Scotland": 190000}


def rpick(choices):
    r, acc = rt.random(), 0.0
    for v, w in choices:
        acc += w
        if r <= acc:
            return v
    return choices[-1][0]


def add_months(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    day = min(d.day, [31, 29 if (d.year + y) % 4 == 0 else 28, 31, 30, 31,
                      30, 31, 31, 30, 31, 30, 31][mo])
    return date(d.year + y, mo + 1, day)


def months_between(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)


def dpd_status(days):
    if days == 0:
        return "Current"
    if days < 30:
        return "1-29 DPD"
    if days < 60:
        return "30-59 DPD"
    if days < 90:
        return "60-89 DPD"
    if days < 180:
        return "90+ DPD"
    return "Default"


tape = []
for i in range(1, 2001):
    region = rpick(REGIONS)
    occupancy = rpick([("Owner-occupied", 0.82), ("Buy-to-let", 0.18)])
    orig = date(2015, 1, 1) + timedelta(days=rt.randint(0, (date(2025, 9, 30) - date(2015, 1, 1)).days))
    term = rt.choice([300, 300, 360, 360, 420]) if occupancy == "Owner-occupied" else rt.choice([240, 300])
    value = round(rt.lognormvariate(math.log(REGION_PRICE[region]), 0.35), -3)
    oltv = min(95.0, max(35.0, rt.gauss(72 if occupancy == "Owner-occupied" else 65, 12)))
    obal = round(value * oltv / 100, 2)
    rate_type = rpick([("Fixed", 0.78), ("Tracker", 0.12), ("SVR", 0.10)])
    rate = round(max(1.2, rt.gauss({"Fixed": 3.9, "Tracker": 5.1, "SVR": 7.2}[rate_type], 0.6)), 2)
    if occupancy == "Buy-to-let":
        repay = rpick([("Interest-only", 0.75), ("Repayment", 0.25)])
    else:
        repay = rpick([("Repayment", 0.93), ("Part and part", 0.07)])
    r = rate / 1200
    seasoning = months_between(orig, CUTOFF)
    if repay == "Interest-only":
        pay = round(obal * r, 2)
        cbal = obal
    else:
        amort_part = obal if repay == "Repayment" else obal * 0.5
        io_part = obal - amort_part
        pay_a = amort_part * r / (1 - (1 + r) ** -term)
        cbal_a = amort_part * (1 + r) ** seasoning - pay_a * ((1 + r) ** seasoning - 1) / r
        pay = round(pay_a + io_part * r, 2)
        cbal = round(max(0.0, cbal_a) + io_part, 2)
    income = round(obal / rt.uniform(3.0, 4.5), -2) if occupancy == "Owner-occupied" else round(obal / rt.uniform(4.0, 6.0), -2)
    u = rt.random()
    days = (0 if u < 0.90 else rt.randint(1, 29) if u < 0.945 else rt.randint(30, 59) if u < 0.965
            else rt.randint(60, 89) if u < 0.977 else rt.randint(90, 179) if u < 0.991 else rt.randint(180, 420))
    tape.append({
        "loan_id": f"M{i:06d}",
        "borrower_id": f"B{i:05d}",
        "origination_date": orig.isoformat(),
        "maturity_date": add_months(orig, term).isoformat(),
        "original_term_months": term,
        "remaining_term_months": term - seasoning,
        "seasoning_months": seasoning,
        "original_balance": obal,
        "current_balance": cbal,
        "interest_rate": rate,
        "rate_type": rate_type,
        "repayment_type": repay,
        "monthly_payment": pay,
        "property_value": value,
        "original_ltv": round(obal / value * 100, 2),
        "current_ltv": round(cbal / value * 100, 2),
        "region": region,
        "property_type": rpick([("Detached", 0.22), ("Semi-detached", 0.30), ("Terraced", 0.28), ("Flat", 0.20)]),
        "occupancy": occupancy,
        "borrower_income": income,
        "first_time_buyer": "Y" if occupancy == "Owner-occupied" and rt.random() < 0.3 else "N",
        "days_in_arrears": days,
        "arrears_balance": round(pay * days / 30, 2) if days else 0.0,
        "status": dpd_status(days),
        "cutoff_date": CUTOFF.isoformat(),
    })

clean_tape = pd.DataFrame(tape)
control = pd.DataFrame([{
    "cutoff_date": CUTOFF.isoformat(),
    "pool_name": "Northbridge Residential Mortgages 2026-1",
    "loan_count": len(clean_tape),
    "total_original_balance": round(clean_tape["original_balance"].sum(), 2),
    "total_current_balance": round(clean_tape["current_balance"].sum(), 2),
    "total_arrears_balance": round(clean_tape["arrears_balance"].sum(), 2),
    "loans_90_plus": int((clean_tape["days_in_arrears"] >= 90).sum()),
}])

# plant the defects on distinct, randomly chosen loans
pool = list(range(len(tape)))
rt.shuffle(pool)


def take(n):
    return [pool.pop() for _ in range(n)]


for k in take(12):
    tape[k]["property_value"] = None
for k in take(5):
    tape[k]["interest_rate"] = None
for k in take(4):
    tape[k]["region"] = None
for k in take(4):
    tape[k]["interest_rate"] = round(tape[k]["interest_rate"] * 100, 0)
for k in take(3):
    tape[k]["status"] = "PERF"
for k in take(3):
    tape[k]["current_balance"] = -tape[k]["current_balance"]
for k in take(5):
    tape[k]["property_value"] = round(tape[k]["property_value"] / 1000, 0)
    tape[k]["current_ltv"] = round(tape[k]["current_balance"] / tape[k]["property_value"] * 100, 2)
for k in take(2):
    tape[k]["origination_date"] = "2026-02-15"
for k in take(4):
    o = date.fromisoformat(tape[k]["origination_date"])
    tape[k]["maturity_date"] = add_months(o, -12).isoformat()
for k in [x for x in take(12) if tape[x]["repayment_type"] == "Repayment"][:6]:
    tape[k]["current_balance"] = round(tape[k]["original_balance"] * 1.08, 2)
for k in take(7):
    tape[k]["days_in_arrears"] = rt.randint(30, 75)
    tape[k]["status"] = "Current"
for k in take(3):
    tape[k]["current_ltv"] = round(tape[k]["current_ltv"] + 11.5, 2)
for k in take(5):
    y, m, d = tape[k]["origination_date"].split("-")
    tape[k]["origination_date"] = f"{d}/{m}/{y}"
for k in take(2):
    other = dict(tape[pool.pop()])
    other["loan_id"] = tape[k]["loan_id"]
    tape.append(other)
for k in take(3):
    tape.append(dict(tape[k]))

tape_df = pd.DataFrame(tape)
tape_df["_order"] = [rt.random() if n >= 2000 else n for n in range(len(tape_df))]
# duplicates sit next to the loan they copy, as they do in real extracts
tape_df["_key"] = tape_df["loan_id"]
tape_df = tape_df.sort_values(["_key", "_order"]).drop(columns=["_order", "_key"])
(DATA / "loan_tape").mkdir(exist_ok=True)
tape_df.to_csv(DATA / "loan_tape" / "loan_tape.csv", index=False,
               lineterminator="\n")
control.to_csv(DATA / "loan_tape" / "loan_tape_control.csv", index=False,
               lineterminator="\n")
TABLES["loan_tape"] = tape_df
TABLES["loan_tape_control"] = control

for name, df in TABLES.items():
    unit = "row" if len(df) == 1 else "rows"
    print(f"{name:<18}{len(df):>7,} {unit}")
print("Files written to", DATA)
