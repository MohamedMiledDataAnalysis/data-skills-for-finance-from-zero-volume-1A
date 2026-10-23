# ex4_threshold.py - Exercise 4: catch 70% of non-performing loans
import statsmodels.formula.api as smf
from sklearn.metrics import confusion_matrix, roc_curve

from regdata import load_loans, split

train, test = split(load_loans())
model = smf.logit("non_performing ~ risk_rating + C(product)",
                  data=train).fit(disp=0)
prob = model.predict(test)
y = test["non_performing"]

fpr, tpr, thresholds = roc_curve(y, prob,
                                 drop_intermediate=False)
ok = tpr >= 0.70
threshold = thresholds[ok][0]
print(f"Highest threshold with recall >= 70%: {threshold:.4f}")
flag = (prob >= threshold).astype(int)
tn, fp, fn, tp = confusion_matrix(y, flag).ravel()
print(f"Caught {tp} of {tp + fn} non-performing "
      f"({tp / (tp + fn):.1%})")
print(f"False alarms: {fp} of {fp + tn} performing "
      f"({fp / (fp + tn):.1%})")
print(f"Loans to review: {tp + fp}")
