# credit_models.py - pricing and arrears models for the committee
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from openpyxl import load_workbook
from openpyxl.styles import Font
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, roc_auc_score)

from regdata import load_loans, split, coef_table

RATE_FORMULA = "interest_rate ~ risk_rating + C(product)"
NP_FORMULA = "non_performing ~ risk_rating + C(product)"
EXCEL_FILE = Path("output") / "credit_models.xlsx"


def fit_models(train):
    rate_model = smf.ols(RATE_FORMULA, data=train).fit()
    np_model = smf.logit(NP_FORMULA, data=train).fit(disp=0)
    return rate_model, np_model


def odds_ratios(model):
    table = coef_table(model)
    out = np.exp(table[["coef", "ci_low", "ci_high"]])
    out.columns = ["odds_ratio", "ci_low", "ci_high"]
    out["p_value"] = table["p_value"]
    return out


def predictions(test, rate_model, np_model, threshold):
    out = test[["loan_id", "product", "risk_rating",
                "interest_rate", "non_performing"]].copy()
    out["predicted_rate"] = rate_model.predict(test)
    out["rate_error"] = (out["interest_rate"]
                         - out["predicted_rate"])
    out["prob_non_performing"] = np_model.predict(test)
    out["flag"] = (out["prob_non_performing"]
                   >= threshold).astype(int)
    return out


def test_metrics(pred, rate_model, threshold):
    err = pred["rate_error"]
    actual = pred["interest_rate"]
    y = pred["non_performing"]
    flag = pred["flag"]
    r2 = 1 - (err ** 2).sum() / ((actual - actual.mean()) ** 2
                                 ).sum()
    rows = [
        ("Training loans", int(rate_model.nobs)),
        ("Test loans", len(pred)),
        ("Rate model: R-squared (training)",
         rate_model.rsquared),
        ("Rate model: R-squared (test)", r2),
        ("Rate model: RMSE (pp)", np.sqrt((err ** 2).mean())),
        ("Rate model: MAE (pp)", err.abs().mean()),
        ("Arrears model: threshold", threshold),
        ("Arrears model: AUC",
         roc_auc_score(y, pred["prob_non_performing"])),
        ("Arrears model: accuracy", accuracy_score(y, flag)),
        ("Arrears model: precision", precision_score(y, flag)),
        ("Arrears model: recall", recall_score(y, flag)),
        ("Non-performing test loans", int(y.sum())),
        ("Flagged test loans", int(flag.sum())),
    ]
    rows = [(name, round(float(value), 4)) if
            isinstance(value, float) else (name, value)
            for name, value in rows]
    return pd.DataFrame(rows, columns=["metric", "value"],
                        dtype=object)


def write_excel(sheets):
    EXCEL_FILE.parent.mkdir(exist_ok=True)
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
        for name, table in sheets.items():
            table.to_excel(writer, sheet_name=name, index=False)
    wb = load_workbook(EXCEL_FILE)
    for ws in wb.worksheets:
        for cell in ws[1]:
            cell.font = Font(bold=True)
        for column in ws.columns:
            letter = column[0].column_letter
            longest = max(len(str(c.value)) for c in column)
            ws.column_dimensions[letter].width = min(longest,
                                                     40) + 4
            for cell in column[1:]:
                if isinstance(cell.value, float):
                    cell.number_format = "#,##0.0000"
        ws.freeze_panes = "A2"
    wb.save(EXCEL_FILE)
    print("Saved", EXCEL_FILE.as_posix())


def main():
    train, test = split(load_loans())
    rate_model, np_model = fit_models(train)
    threshold = train["non_performing"].mean()

    linear = coef_table(rate_model).reset_index(names="term")
    logistic = odds_ratios(np_model).reset_index(names="term")
    pred = predictions(test, rate_model, np_model, threshold)
    metrics = test_metrics(pred, rate_model, threshold)

    write_excel({"LinearCoefficients": linear,
                 "LogisticOddsRatios": logistic,
                 "TestMetrics": metrics,
                 "Predictions": pred})

    for metric, value in metrics.itertuples(index=False):
        print(f"{metric:<34}{value:>8}")


if __name__ == "__main__":
    main()
