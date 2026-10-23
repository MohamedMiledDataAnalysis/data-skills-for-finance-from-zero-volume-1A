from monthly_report import (load_accounts, load_fx,
                            last_rate_date, convert_to_gbp)

fx = load_fx()
accounts = load_accounts()
day = last_rate_date(fx, "2025-12")
accounts = convert_to_gbp(accounts, fx, day)

deposits = (accounts.groupby("currency")
            .agg(accounts=("account_id", "count"),
                 balance=("balance", "sum"),
                 balance_gbp=("balance_gbp", "sum"))
            .round(2))
deposits["share_pct"] = (deposits["balance_gbp"]
                         / deposits["balance_gbp"].sum()
                         * 100).round(1)
print(deposits)
print("Total GBP equivalent:",
      f"£{deposits['balance_gbp'].sum():,.2f}")
