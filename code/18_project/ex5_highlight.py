from openpyxl import load_workbook
from openpyxl.styles import PatternFill

import monthly_report

monthly_report.main()

fills = {"Default": PatternFill("solid", fgColor="F2D7DB"),
         "90+ DPD": PatternFill("solid", fgColor="F5EBD0")}

wb = load_workbook(monthly_report.EXCEL_FILE)
ws = wb["Arrears"]
headers = [cell.value for cell in ws[1]]
status_col = headers.index("status")
counts = {"Default": 0, "90+ DPD": 0}
for row in ws.iter_rows(min_row=2):
    status = row[status_col].value
    if status in fills:
        counts[status] += 1
        for cell in row:
            cell.fill = fills[status]
ws.auto_filter.ref = ws.dimensions
wb.save(monthly_report.EXCEL_FILE)
print("Highlighted rows:", counts)
print("Filter range:", ws.auto_filter.ref)
