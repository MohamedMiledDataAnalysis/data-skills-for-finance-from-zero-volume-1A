"""
tapecheck.py - load, check, reconcile, clean and stratify a
residential mortgage loan tape.

Import it from a script in the same folder:

    from tapecheck import load_tape, profile, RULES, run_checks
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

# Reuse the chart style from Chapter 17.
sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import (nb_style, add_titles, save_chart, pct,
                      PALETTE)

TAPE_FILE = "data/loan_tape/loan_tape.csv"
CONTROL_FILE = "data/loan_tape/loan_tape_control.csv"
CUTOFF = pd.Timestamp("2025-12-31")
OUTPUT = Path("output")

NUMERIC = ["original_term_months", "remaining_term_months",
           "seasoning_months", "original_balance",
           "current_balance", "interest_rate", "monthly_payment",
           "property_value", "original_ltv", "current_ltv",
           "borrower_income", "days_in_arrears", "arrears_balance"]
DATES = ["origination_date", "maturity_date", "cutoff_date"]
STATUSES = ["Current", "1-29 DPD", "30-59 DPD", "60-89 DPD",
            "90+ DPD", "Default"]
MANDATORY = ["loan_id", "borrower_id", "maturity_date",
             "original_term_months",
             "original_balance", "current_balance",
             "repayment_type", "occupancy", "days_in_arrears",
             "status", "cutoff_date"]


# ------------------------------------------------------- loading
def load_tape(path=TAPE_FILE):
    raw = pd.read_csv(path, dtype=str)
    tape = raw.copy()
    tape["origination_raw"] = raw["origination_date"]
    for col in NUMERIC:
        tape[col] = pd.to_numeric(raw[col], errors="coerce")
    for col in DATES:
        tape[col] = pd.to_datetime(raw[col], format="%Y-%m-%d",
                                   errors="coerce")
    return raw, tape


def profile(df):
    rows = []
    for col in df.columns:
        s = df[col]
        numeric = pd.api.types.is_numeric_dtype(s)
        rows.append({
            "column": col,
            "dtype": str(s.dtype),
            "missing": int(s.isna().sum()),
            "distinct": int(s.nunique()),
            "min": s.min() if numeric else "",
            "max": s.max() if numeric else "",
        })
    return pd.DataFrame(rows)


# ------------------------------------------------------- rules
def dpd_bucket(days):
    bins = [-1, 0, 29, 59, 89, 179, float("inf")]
    return pd.cut(days, bins=bins, labels=STATUSES)


def ltv_gap(t):
    calc = t["current_balance"] / t["property_value"] * 100
    return (t["current_ltv"] - calc).abs() > 0.5


RULES = [
    {"rule_id": "DQ01", "dimension": "Uniqueness",
     "severity": "Critical", "fields": ["loan_id"],
     "description": "Exact duplicate row",
     "test": lambda t: t.duplicated()},
    {"rule_id": "DQ02", "dimension": "Uniqueness",
     "severity": "Critical", "fields": ["loan_id", "borrower_id"],
     "description": "loan_id reused by a different record",
     "test": lambda t: t["loan_id"].duplicated(keep=False)
                       & ~t.duplicated(keep=False)},
    {"rule_id": "DQ03", "dimension": "Completeness",
     "severity": "Warning", "fields": ["property_value"],
     "description": "property_value blank",
     "test": lambda t: t["property_value"].isna()},
    {"rule_id": "DQ04", "dimension": "Completeness",
     "severity": "Warning", "fields": ["interest_rate"],
     "description": "interest_rate blank",
     "test": lambda t: t["interest_rate"].isna()},
    {"rule_id": "DQ05", "dimension": "Completeness",
     "severity": "Warning", "fields": ["region"],
     "description": "region blank",
     "test": lambda t: t["region"].isna()},
    {"rule_id": "DQ06", "dimension": "Completeness",
     "severity": "Critical", "fields": ["loan_id"],
     "description": "Another mandatory field blank",
     "test": lambda t: t[MANDATORY].isna().any(axis=1)},
    {"rule_id": "DQ07", "dimension": "Validity",
     "severity": "Critical", "fields": ["interest_rate"],
     "description": "interest_rate outside 0-15%",
     "test": lambda t: t["interest_rate"].notna()
                       & ~t["interest_rate"].between(0, 15)},
    {"rule_id": "DQ08", "dimension": "Validity",
     "severity": "Warning", "fields": ["status"],
     "description": "status not in the allowed list",
     "test": lambda t: ~t["status"].isin(STATUSES)},
    {"rule_id": "DQ09", "dimension": "Validity",
     "severity": "Critical", "fields": ["current_balance"],
     "description": "current_balance negative",
     "test": lambda t: t["current_balance"] < 0},
    {"rule_id": "DQ10", "dimension": "Validity",
     "severity": "Critical",
     "fields": ["current_ltv", "property_value"],
     "description": "current_ltv above 150%",
     "test": lambda t: t["current_ltv"] > 150},
    {"rule_id": "DQ11", "dimension": "Validity",
     "severity": "Warning", "fields": ["origination_raw"],
     "description": "origination_date not YYYY-MM-DD",
     "test": lambda t: t["origination_date"].isna()},
    {"rule_id": "DQ12", "dimension": "Timeliness",
     "severity": "Critical", "fields": ["origination_raw"],
     "description": "origination_date after the cut-off",
     "test": lambda t: t["origination_date"] > CUTOFF},
    {"rule_id": "DQ13", "dimension": "Timeliness",
     "severity": "Critical", "fields": ["cutoff_date"],
     "description": "cutoff_date differs from CUTOFF",
     "test": lambda t: t["cutoff_date"] != CUTOFF},
    {"rule_id": "DQ14", "dimension": "Consistency",
     "severity": "Critical",
     "fields": ["origination_raw", "maturity_date"],
     "description": "maturity_date not after origination",
     "test": lambda t: t["maturity_date"]
                       <= t["origination_date"]},
    {"rule_id": "DQ15", "dimension": "Consistency",
     "severity": "Critical",
     "fields": ["original_balance", "current_balance"],
     "description": "current_balance above original_balance",
     "test": lambda t: t["current_balance"]
                       > t["original_balance"]},
    {"rule_id": "DQ16", "dimension": "Consistency",
     "severity": "Warning",
     "fields": ["status", "days_in_arrears"],
     "description": "status disagrees with days_in_arrears",
     "test": lambda t: t["status"].isin(STATUSES)
                       & (t["status"].astype(str) != dpd_bucket(
                           t["days_in_arrears"]).astype(str))},
    {"rule_id": "DQ17", "dimension": "Consistency",
     "severity": "Warning",
     "fields": ["current_ltv", "current_balance",
                "property_value"],
     "description": "current_ltv != balance / value",
     "test": ltv_gap},
    {"rule_id": "DQ18", "dimension": "Consistency",
     "severity": "Warning",
     "fields": ["original_term_months",
                "remaining_term_months", "seasoning_months"],
     "description": "remaining + seasoning != original term",
     "test": lambda t: t["remaining_term_months"]
                       + t["seasoning_months"]
                       != t["original_term_months"]},
]


def failing(rule, tape):
    return rule["test"](tape).fillna(False).astype(bool)


def as_text(value):
    if pd.isna(value):
        return "(blank)"
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    return str(value)


def run_checks(tape, rules):
    summary, exceptions = [], []
    for rule in rules:
        failed = failing(rule, tape)
        summary.append({
            "rule_id": rule["rule_id"],
            "dimension": rule["dimension"],
            "severity": rule["severity"],
            "description": rule["description"],
            "failed_rows": int(failed.sum()),
            "result": "Fail" if failed.any() else "Pass",
        })
        for idx, row in tape[failed].iterrows():
            values = "; ".join(f"{f}={as_text(row[f])}"
                               for f in rule["fields"])
            exceptions.append({"loan_id": row["loan_id"],
                               "file_row": idx + 2,
                               "rule_id": rule["rule_id"],
                               "values": values})
    return pd.DataFrame(summary), pd.DataFrame(exceptions)


# ------------------------------------------------------- Excel
def format_workbook(path):
    wb = load_workbook(path)
    fill = PatternFill("solid", fgColor="1F2A44")
    for ws in wb.worksheets:
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = fill
        for column in ws.columns:
            letter = column[0].column_letter
            longest = max(len(str(c.value)) for c in column)
            ws.column_dimensions[letter].width = min(longest + 3,
                                                     60)
            for cell in column[1:]:
                if isinstance(cell.value, float):
                    cell.number_format = "#,##0.00"
                elif isinstance(cell.value, int):
                    cell.number_format = "#,##0"
        ws.freeze_panes = "A2"
    wb.save(path)


def write_workbook(path, sheets):
    OUTPUT.mkdir(exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, table in sheets.items():
            table.to_excel(writer, sheet_name=name, index=False)
    format_workbook(path)
    print("Saved", Path(path).as_posix())


# ------------------------------------------------ reconciliation
def totals(df):
    return pd.Series({
        "loan_count": len(df),
        "total_original_balance": df["original_balance"].sum(),
        "total_current_balance": df["current_balance"].sum(),
        "total_arrears_balance": df["arrears_balance"].sum(),
        "loans_90_plus": (df["days_in_arrears"] >= 90).sum(),
    })


def reconcile(tape, control):
    raw_totals = totals(tape)
    table = pd.DataFrame({
        "raw": raw_totals,
        "dedup": totals(tape.drop_duplicates()),
        "control": control.iloc[0][raw_totals.index],
    }).astype(float)
    table["diff"] = table["dedup"] - table["control"]
    return table.round(2)


# ------------------------------------------------------ cleaning
def clean_tape(tape, rules):
    log = []
    dup = tape.duplicated()
    for loan in tape.loc[dup, "loan_id"]:
        log.append({"loan_id": loan, "action": "Dropped",
                    "field": "(row)", "old": "", "new": "",
                    "reason": "DQ01 exact duplicate"})
    clean = tape[~dup].copy()

    perf = clean["status"] == "PERF"
    for loan in clean.loc[perf, "loan_id"]:
        log.append({"loan_id": loan, "action": "Corrected",
                    "field": "status", "old": "PERF",
                    "new": "Current",
                    "reason": "DQ08 legacy code for Current"})
    clean["status"] = clean["status"].where(~perf, "Current")

    rate = clean["interest_rate"]
    bp = rate > 15
    for loan, old in rate[bp].items():
        log.append({"loan_id": clean.loc[loan, "loan_id"],
                    "action": "Corrected",
                    "field": "interest_rate", "old": old,
                    "new": old / 100,
                    "reason": "DQ07 keyed in basis points"})
    clean["interest_rate"] = rate.where(~bp, rate / 100)

    critical = [r for r in rules if r["severity"] == "Critical"]
    failed = pd.DataFrame({r["rule_id"]: failing(r, clean)
                           for r in critical})
    out = failed.any(axis=1)
    quarantine = clean[out].copy()
    quarantine["failed_rules"] = failed[out].apply(
        lambda row: ", ".join(row[row].index), axis=1)
    for _, row in quarantine.iterrows():
        log.append({"loan_id": row["loan_id"],
                    "action": "Quarantined", "field": "(row)",
                    "old": "", "new": "",
                    "reason": row["failed_rules"]})
    return clean[~out].copy(), quarantine, pd.DataFrame(log)


# ------------------------------------------------ stratification
def wavg(values, weights):
    known = values.notna()
    total = weights[known].sum()
    if total == 0:
        return float("nan")
    return (values[known] * weights[known]).sum() / total


def strat_row(band, g, n_all, bal_all):
    bal = g["current_balance"]
    return {"band": band,
            "loans": len(g),
            "pct_loans": len(g) / n_all * 100,
            "balance": bal.sum(),
            "pct_balance": bal.sum() / bal_all * 100,
            "wa_rate": wavg(g["interest_rate"], bal),
            "wa_ltv": wavg(g["current_ltv"], bal),
            "wa_seasoning": wavg(g["seasoning_months"], bal)}


def stratify(df, column, bins=None, labels=None,
             right=True):
    data = df.copy()
    if bins is None:
        band = pd.Series(pd.Categorical(data[column],
                                        categories=labels),
                         index=data.index)
    else:
        band = pd.cut(data[column], bins=bins, labels=labels,
                      right=right, include_lowest=True)
    if band.isna().any():
        band = band.cat.add_categories("Unknown")
        band = band.fillna("Unknown")
    data["band"] = band
    n_all = len(data)
    bal_all = data["current_balance"].sum()
    groups = data.groupby("band", observed=False)
    rows = [strat_row(name, g, n_all, bal_all)
            for name, g in groups]
    rows.append(strat_row("Total", data, n_all, bal_all))
    return pd.DataFrame(rows)


def show(table):
    view = pd.DataFrame({
        "band": table["band"].astype(str),
        "loans": table["loans"],
        "%loans": table["pct_loans"].round(1),
        "bal_£m": (table["balance"] / 1e6).round(1),
        "%bal": table["pct_balance"].round(1),
        "rate": table["wa_rate"].round(2),
        "ltv": table["wa_ltv"].round(1),
        "seas": table["wa_seasoning"].map(
            lambda v: "-" if pd.isna(v) else f"{v:.0f}"),
    })
    return view.to_string(index=False, na_rep="-")


INF = float("inf")
LTV_BINS = [0, 50, 60, 70, 80, 90, 100, INF]
LTV_LABELS = ["0-50", "50-60", "60-70", "70-80", "80-90",
              "90-100", ">100"]


def standard_strats(clean):
    df = clean.copy()
    df["seasoning_years"] = df["seasoning_months"] / 12
    df["dpd_bucket"] = dpd_bucket(df["days_in_arrears"])
    regions = (df.groupby("region")["current_balance"].sum()
               .sort_values(ascending=False).index.tolist())
    return {
        "LTV": stratify(df, "current_ltv", LTV_BINS, LTV_LABELS),
        "Region": stratify(df, "region", labels=regions),
        "Rate": stratify(
            df, "interest_rate",
            [0, 3, 3.5, 4, 4.5, 5, 6, 7, INF],
            ["0-3.0", "3.0-3.5", "3.5-4.0", "4.0-4.5",
             "4.5-5.0", "5.0-6.0", "6.0-7.0", ">7.0"]),
        "Seasoning": stratify(
            df, "seasoning_years", [0, 1, 2, 3, 5, 7, 10, INF],
            ["<1", "1-2", "2-3", "3-5", "5-7", "7-10", "10+"],
            right=False),
        "Repayment": stratify(
            df, "repayment_type",
            labels=["Repayment", "Part and part",
                    "Interest-only"]),
        "Occupancy": stratify(
            df, "occupancy",
            labels=["Owner-occupied", "Buy-to-let"]),
        "Arrears": stratify(df, "dpd_bucket", labels=STATUSES),
    }


# -------------------------------------------------- pool summary
def pool_summary(df):
    bal = df["current_balance"]
    total = bal.sum()
    by_region = df.groupby("region")["current_balance"].sum()
    io = df["repayment_type"] == "Interest-only"
    btl = df["occupancy"] == "Buy-to-let"
    late = df["days_in_arrears"] >= 90
    items = {
        "Number of loans": len(df),
        "Total current balance (GBP)": total,
        "Average current balance (GBP)": bal.mean(),
        "Largest current balance (GBP)": bal.max(),
        "WA interest rate (%)": wavg(df["interest_rate"], bal),
        "WA current LTV (%)": wavg(df["current_ltv"], bal),
        "WA original LTV (%)": wavg(df["original_ltv"], bal),
        "WA seasoning (months)": wavg(df["seasoning_months"], bal),
        "WA remaining term (months)": wavg(
            df["remaining_term_months"], bal),
        "Interest-only (% balance)": bal[io].sum() / total * 100,
        "Buy-to-let (% balance)": bal[btl].sum() / total * 100,
        "90+ days in arrears (% balance)":
            bal[late].sum() / total * 100,
        "Largest region": by_region.idxmax(),
        "Largest region (% balance)":
            by_region.max() / total * 100,
    }
    values = [round(v, 2) if isinstance(v, float) else v
              for v in items.values()]
    return pd.DataFrame({"metric": list(items), "value": values})


def fmt(value):
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


# -------------------------------------------------------- charts
def bar_chart(table, title, xlabel, filename, book_name,
              horizontal=False, colours=None):
    nb_style()
    data = table[table["band"] != "Total"]
    labels = data["band"].astype(str)
    colours = colours or PALETTE["navy"]
    if horizontal:
        fig, ax = plt.subplots(figsize=(5.4, 3.8))
        bars = ax.barh(labels, data["pct_balance"],
                       color=colours, height=0.6)
        ax.xaxis.set_major_formatter(pct)
        ax.set_xlim(0, data["pct_balance"].max() * 1.18)
        ax.set_xlabel(xlabel)
        ax.grid(axis="y", visible=False)
    else:
        fig, ax = plt.subplots(figsize=(6, 3.4))
        bars = ax.bar(labels, data["pct_balance"],
                      color=colours, width=0.6)
        ax.yaxis.set_major_formatter(pct)
        ax.set_ylim(0, data["pct_balance"].max() * 1.18)
        ax.set_ylabel("Share of current balance (%)")
        ax.set_xlabel(xlabel)
        ax.grid(axis="x", visible=False)
    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=8)
    add_titles(ax, title)
    save_chart(fig, filename, book_name)
    plt.close(fig)


def make_charts(strats):
    bar_chart(strats["LTV"], "Pool balance by current LTV band",
              "Current LTV band (%)", "ch19_ltv.png",
              "ch19-ltv.png")
    region = strats["Region"].sort_values("pct_balance")
    bar_chart(region, "Regional concentration of the pool",
              "Share of current balance (%)", "ch19_region.png",
              "ch19-region.png", horizontal=True)
    late = strats["Arrears"].iloc[1:]
    colours = [PALETTE["red"] if b in ("90+ DPD", "Default")
               else PALETTE["navy"] for b in late["band"]
               if b != "Total"]
    bar_chart(late, "Loans in arrears, by days past due",
              "Bucket from days_in_arrears (red: 90 days or more)",
              "ch19_arrears.png", "ch19-arrears.png",
              colours=colours)
