# ex3_eurgbp.py - Exercise 3: EUR/GBP returns, volatility, VaR
import numpy as np
import pandas as pd

fx = pd.read_csv("data/csv/fx_rates.csv", parse_dates=["rate_date"])
eur = (fx[fx["currency"] == "EUR"]
       .set_index("rate_date").sort_index())
gbp_per_eur = 1 / eur["rate_per_gbp"]      # value of €1 in £
log_ret = np.log(gbp_per_eur).diff().dropna()
simple = gbp_per_eur.pct_change().dropna()

print(len(log_ret))
print(round(gbp_per_eur.iloc[0], 4), round(gbp_per_eur.iloc[-1], 4))
change = gbp_per_eur.iloc[-1] / gbp_per_eur.iloc[0] - 1
print(f"2025 change:       {100 * change:.3f}%")
daily_sd = log_ret.std()
print(f"Daily volatility:  {100 * daily_sd:.4f}%")
print(f"Annual volatility: {100 * daily_sd * np.sqrt(261):.4f}%")
print(f"Worst day:         {100 * log_ret.min():.4f}%"
      f" on {log_ret.idxmin().date()}")

EXPOSURE_EUR = 5_000_000         # a €5m receivable
value_gbp = EXPOSURE_EUR * gbp_per_eur.iloc[-1]
var95 = -simple.quantile(0.05) * value_gbp
print(f"Value today: £{value_gbp:,.0f}; 95% VaR: £{var95:,.0f}")
