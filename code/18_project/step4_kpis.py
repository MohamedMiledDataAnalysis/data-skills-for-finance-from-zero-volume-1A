import pandas as pd

from monthly_report import load_loans, kpis, kpis_by

pd.options.display.float_format = "{:,.2f}".format

loans = load_loans()
print(kpis(loans))
print(kpis_by(loans, "product"))
