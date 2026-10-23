from monthly_report import (load_accounts, load_fx,
                            last_rate_date, convert_to_gbp)

fx = load_fx()
accounts = load_accounts()
for month in ["2025-06", "2025-12"]:
    day = last_rate_date(fx, month)
    converted = convert_to_gbp(accounts, fx, day)
    total = converted["balance_gbp"].sum()
    print(f"{month}: rate date {day.date()}, "
          f"deposits £{total:,.2f}")
