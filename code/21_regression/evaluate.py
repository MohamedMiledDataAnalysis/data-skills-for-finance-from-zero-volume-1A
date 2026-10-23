# evaluate.py - judge the logistic model on the test set
import statsmodels.formula.api as smf
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_score, recall_score,
                             roc_auc_score)

from regdata import load_loans, split

train, test = split(load_loans())
model = smf.logit("non_performing ~ risk_rating + C(product)",
                  data=train).fit(disp=0)
test["prob"] = model.predict(test)
actual = test["non_performing"]
base_rate = train["non_performing"].mean()

for threshold in [0.5, base_rate]:
    flag = (test["prob"] >= threshold).astype(int)
    print(f"Threshold {threshold:.4f}")
    print(confusion_matrix(actual, flag))
    print(f"  accuracy  {accuracy_score(actual, flag):.3f}")
    print(f"  precision "
          f"{precision_score(actual, flag, zero_division=0):.3f}")
    print(f"  recall    {recall_score(actual, flag):.3f}")

everyone_ok = [0] * len(test)
print("Accuracy, all Performing:",
      f"{accuracy_score(actual, everyone_ok):.3f}")
print(f"AUC: {roc_auc_score(actual, test['prob']):.3f}")
