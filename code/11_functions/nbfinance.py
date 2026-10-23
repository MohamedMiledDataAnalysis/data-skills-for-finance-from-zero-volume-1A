"""nbfinance - Northbridge Bank loan calculations.

Functions:
    monthly_payment     fixed monthly repayment of an annuity loan
    amortisation        full repayment schedule, one row per month
    dpd_bucket          arrears bucket for a number of days past due
    months_between      whole months between two dates
"""


def monthly_payment(principal, annual_rate_pct, term_months):
    """Return the fixed monthly repayment of an annuity loan.

    principal        amount borrowed, in pounds (> 0)
    annual_rate_pct  interest rate in per cent a year (4.5 = 4.5%)
    term_months      number of monthly repayments (> 0)
    """
    if principal <= 0:
        raise ValueError(f"principal must be > 0, got {principal}")
    if term_months <= 0:
        raise ValueError(
            f"term_months must be > 0, got {term_months}"
        )
    if annual_rate_pct < 0:
        raise ValueError(
            f"annual_rate_pct must be >= 0, got {annual_rate_pct}"
        )
    r = annual_rate_pct / 100 / 12
    if r == 0:
        return principal / term_months
    return principal * r / (1 - (1 + r) ** -term_months)


def amortisation(principal, annual_rate_pct, term_months):
    """Return the repayment schedule as a list of dictionaries.

    Each row has: period, opening, interest, principal, closing.
    Amounts are rounded to the penny; the last payment is
    adjusted so that the closing balance is exactly 0.00.
    """
    payment = round(
        monthly_payment(principal, annual_rate_pct, term_months), 2
    )
    r = annual_rate_pct / 100 / 12
    balance = principal
    rows = []
    for period in range(1, term_months + 1):
        interest = round(balance * r, 2)
        repaid = round(payment - interest, 2)
        if period == term_months:      # final payment
            repaid = balance
        closing = round(balance - repaid, 2)
        rows.append({
            "period": period,
            "opening": balance,
            "interest": interest,
            "principal": repaid,
            "closing": closing,
        })
        balance = closing
    return rows


def dpd_bucket(days_past_due):
    """Return the collections arrears bucket for a DPD count.

    Buckets: Performing, Early arrears, 30+ DPD, 90+ DPD.
    """
    if days_past_due < 0:
        raise ValueError(
            f"days_past_due must be >= 0, got {days_past_due}"
        )
    if days_past_due == 0:
        return "Performing"
    elif days_past_due < 30:
        return "Early arrears"
    elif days_past_due < 90:
        return "30+ DPD"
    return "90+ DPD"


def months_between(start, end):
    """Return the number of whole months from start to end.

    start, end   datetime.date objects, with start <= end
    """
    if end < start:
        raise ValueError(f"end {end} is before start {start}")
    months = (end.year - start.year) * 12 + end.month - start.month
    if end.day < start.day:
        months -= 1
    return months


if __name__ == "__main__":
    # Quick self-test, run only when this file is run directly
    print(f"{monthly_payment(250000, 4.5, 300):.2f}")
    print(dpd_bucket(0), dpd_bucket(45), dpd_bucket(120))
