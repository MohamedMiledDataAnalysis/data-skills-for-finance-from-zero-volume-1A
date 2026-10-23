"""
monthly_report.py - Northbridge Bank monthly portfolio report.

Run from the northbridge/ folder:
    python code/18_project/monthly_report.py
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Font

# Reuse the chart style from Chapter 17.
sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import (nb_style, add_titles, save_chart,
                      gbp_m, pct, PALETTE)

REPORT_MONTH = "2025-12"
API_URL = "http://127.0.0.1:8000/fx-rates"
OUTPUT = Path("output")
EXCEL_FILE = OUTPUT / f"northbridge_report_{REPORT_MONTH}.xlsx"
STATUSES = ["Performing", "30+ DPD", "90+ DPD", "Default"]


# ---------------------------------------------------------- step 1
def load_loans():
    loans = pd.read_csv("data/csv/loans.csv",
                        parse_dates=["origination_date"])
    print(f"Loans read from CSV: {len(loans)} rows")
    return loans


def load_customers():
    customers = pd.read_excel("data/excel/northbridge.xlsx",
                              sheet_name="customers")
    print(f"Customers read from Excel: {len(customers)} rows")
    return customers


def load_fx():
    try:
        frames = []
        for currency in ["EUR", "USD"]:
            response = requests.get(API_URL,
                                    params={"currency": currency},
                                    timeout=5)
            response.raise_for_status()
            frames.append(pd.DataFrame(response.json()["rates"]))
        fx = pd.concat(frames, ignore_index=True)
        fx = fx.rename(columns={"date": "rate_date"})
        print(f"FX rates read from the API: {len(fx)} rows")
    except requests.exceptions.RequestException:
        print("The API is not running: FX rates read from "
              "data/csv/fx_rates.csv instead.")
        fx = pd.read_csv("data/csv/fx_rates.csv")
    fx["rate_date"] = pd.to_datetime(fx["rate_date"])
    return fx


def load_accounts():
    with open("data/json/customers.json", encoding="utf-8") as f:
        raw = json.load(f)
    accounts = pd.json_normalize(raw, record_path="accounts",
                                 meta=["customer_id", "segment"])
    print(f"Accounts read from JSON: {len(accounts)} rows")
    return accounts


# ---------------------------------------------------------- step 2
def check_data(loans, customers, accounts, fx):
    assert loans["loan_id"].is_unique, "Duplicate loan_id found"
    assert loans["principal"].notna().all(), "Missing principal"
    assert (loans["principal"] > 0).all(), "Principal must be > 0"
    unknown = set(loans["status"]) - set(STATUSES)
    assert not unknown, f"Unknown loan status: {unknown}"
    orphans = ~loans["customer_id"].isin(customers["customer_id"])
    assert not orphans.any(), (
        f"{orphans.sum()} loans have no matching customer")
    needed = set(accounts["currency"]) - {"GBP"}
    missing = needed - set(fx["currency"])
    assert not missing, f"No FX rate for {missing}"
    print("Data-quality checks passed")


# ---------------------------------------------------------- step 3
def last_rate_date(fx, month):
    in_month = fx[fx["rate_date"].dt.strftime("%Y-%m") == month]
    assert not in_month.empty, f"No FX rates for {month}"
    return in_month["rate_date"].max()


def convert_to_gbp(accounts, fx, rate_day):
    rates = fx[fx["rate_date"] == rate_day]
    rates = rates.set_index("currency")["rate_per_gbp"]
    rates["GBP"] = 1.0
    accounts = accounts.copy()
    accounts["rate_per_gbp"] = accounts["currency"].map(rates)
    accounts["balance_gbp"] = (accounts["balance"]
                               / accounts["rate_per_gbp"]).round(2)
    return accounts


# ---------------------------------------------------------- step 4
def kpis(df):
    principal = df["principal"].sum()
    weighted = (df["principal"] * df["interest_rate"]).sum()
    not_perf = df.loc[df["status"] != "Performing", "principal"]
    return pd.Series({
        "loan_count": len(df),
        "total_principal": principal,
        "wavg_rate_pct": weighted / principal,
        "arrears_rate_pct": not_perf.sum() / principal * 100,
    })


def kpis_by(loans, column):
    rows = {name: kpis(group)
            for name, group in loans.groupby(column)}
    table = pd.DataFrame(rows).T
    table["loan_count"] = table["loan_count"].astype(int)
    table.index.name = column
    return table.reset_index()


# ---------------------------------------------------------- step 5
def write_excel(summary, by_product, by_segment, arrears):
    OUTPUT.mkdir(exist_ok=True)
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        by_product.to_excel(writer, sheet_name="ByProduct",
                            index=False)
        by_segment.to_excel(writer, sheet_name="BySegment",
                            index=False)
        arrears.to_excel(writer, sheet_name="Arrears", index=False)
    print("Saved", EXCEL_FILE.as_posix())


def format_excel(chart_path):
    wb = load_workbook(EXCEL_FILE)
    for ws in wb.worksheets:
        for cell in ws[1]:
            cell.font = Font(bold=True)
        for column in ws.columns:
            letter = column[0].column_letter
            longest = max(len(str(c.value)) for c in column)
            ws.column_dimensions[letter].width = longest + 4
            for cell in column[1:]:
                if isinstance(cell.value, float):
                    cell.number_format = "#,##0.00"
                elif isinstance(cell.value, int):
                    cell.number_format = "#,##0"
        ws.freeze_panes = "A2"
    picture = Image(chart_path)
    ratio = picture.height / picture.width
    picture.width = 600
    picture.height = round(600 * ratio)
    wb["Summary"].add_image(picture, "D2")
    wb.save(EXCEL_FILE)
    print("Formatted", EXCEL_FILE.as_posix())


# ---------------------------------------------------------- step 6
def make_charts(by_product, by_segment):
    nb_style()
    data = by_product.set_index("product")
    data = data.sort_values("total_principal")
    fig, ax = plt.subplots(figsize=(6, 3.3))
    bars = ax.barh(data.index, data["total_principal"] / 1e6,
                   color=PALETTE["navy"], height=0.55)
    ax.bar_label(bars, fmt="£%.1fm", padding=4, fontsize=8)
    ax.xaxis.set_major_formatter(gbp_m)
    ax.set_xlim(0, data["total_principal"].max() / 1e6 * 1.15)
    ax.set_xlabel("Total principal (£ millions)")
    ax.grid(axis="y", visible=False)
    month_name = pd.Timestamp(REPORT_MONTH).strftime("%B %Y")
    add_titles(ax, f"Loan book by product, {month_name}")
    save_chart(fig, "ch18_principal.png", "ch18-principal.png")

    seg = by_segment.set_index("segment")
    seg = seg.sort_values("arrears_rate_pct")
    fig, ax = plt.subplots(figsize=(6, 3))
    bars = ax.barh(seg.index, seg["arrears_rate_pct"],
                   color=PALETTE["red"], height=0.5)
    ax.bar_label(bars, fmt="%.2f%%", padding=4, fontsize=8)
    ax.xaxis.set_major_formatter(pct)
    ax.set_xlim(0, seg["arrears_rate_pct"].max() * 1.2)
    ax.set_xlabel("Principal not performing (%)")
    ax.grid(axis="y", visible=False)
    add_titles(ax, "Arrears rate by customer segment")
    save_chart(fig, "ch18_arrears.png", "ch18-arrears.png")
    plt.close("all")
    return OUTPUT / "ch18_principal.png"


# ---------------------------------------------------------- main
def main():
    loans = load_loans()
    customers = load_customers()
    fx = load_fx()
    accounts = load_accounts()
    check_data(loans, customers, accounts, fx)

    rate_day = last_rate_date(fx, REPORT_MONTH)
    print("FX rate date:", rate_day.date())
    accounts = convert_to_gbp(accounts, fx, rate_day)

    loans = loans.merge(
        customers[["customer_id", "first_name", "last_name",
                   "segment"]], on="customer_id", how="left")
    total = kpis(loans)
    by_product = kpis_by(loans, "product")
    by_segment = kpis_by(loans, "segment")

    arrears = loans[loans["status"] != "Performing"].copy()
    arrears["status"] = pd.Categorical(arrears["status"],
                                       STATUSES, ordered=True)
    arrears = arrears.sort_values(["status", "principal"],
                                  ascending=[False, False])
    arrears["origination_date"] = (
        arrears["origination_date"].dt.date)
    arrears = arrears[["loan_id", "customer_id", "first_name",
                       "last_name", "segment", "product",
                       "principal", "interest_rate", "status",
                       "origination_date"]]
    arrears["status"] = arrears["status"].astype(str)

    summary = pd.DataFrame({
        "metric": ["Report month", "FX rate date", "Loan count",
                   "Total principal (GBP)",
                   "Weighted average rate (%)",
                   "Arrears rate (% of principal)",
                   "Accounts", "Deposits (GBP equivalent)"],
        "value": [REPORT_MONTH, str(rate_day.date()),
                  int(total["loan_count"]),
                  round(total["total_principal"], 2),
                  round(total["wavg_rate_pct"], 2),
                  round(total["arrears_rate_pct"], 2),
                  len(accounts),
                  round(accounts["balance_gbp"].sum(), 2)],
    })

    print()
    print(summary.to_string(index=False))
    print()
    print(by_product.round(2).to_string(index=False))
    print()
    print(by_segment.round(2).to_string(index=False))
    print()

    chart = make_charts(by_product, by_segment)
    write_excel(summary, by_product.round(2),
                by_segment.round(2), arrears)
    format_excel(chart)


if __name__ == "__main__":
    main()
