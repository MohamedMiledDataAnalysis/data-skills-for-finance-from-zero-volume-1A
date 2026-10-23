from monthly_report import (load_fx, load_accounts,
                            last_rate_date, convert_to_gbp)

fx = load_fx()
accounts = load_accounts()
day = last_rate_date(fx, "2025-12")
print("Last rate date in December:", day.date())
print(fx[fx["rate_date"] == day])
converted = convert_to_gbp(accounts, fx, day)
print(converted[["account_id", "currency", "balance",
                 "rate_per_gbp", "balance_gbp"]].head(4))
