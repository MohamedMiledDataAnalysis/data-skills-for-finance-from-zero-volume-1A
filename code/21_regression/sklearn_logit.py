# sklearn_logit.py - the same logistic model with scikit-learn
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression

from regdata import load_loans, split


def features(df):
    X = pd.get_dummies(df["product"], drop_first=True,
                       dtype=int)
    X.insert(0, "risk_rating", df["risk_rating"])
    return X


train, test = split(load_loans())
X_train = features(train)
y_train = train["non_performing"]
print(X_train.head(3))

clf = LogisticRegression(C=np.inf, solver="newton-cholesky",
                         tol=1e-8)
clf.fit(X_train, y_train)

sm = smf.logit("non_performing ~ risk_rating + C(product)",
               data=train).fit(disp=0)
compare = pd.DataFrame({
    "sklearn": [clf.intercept_[0], *clf.coef_[0]],
    "statsmodels": [sm.params["Intercept"],
                    sm.params["risk_rating"],
                    sm.params["C(product)[T.Mortgage]"],
                    sm.params["C(product)[T.Personal]"],
                    sm.params["C(product)[T.SME]"]]},
    index=["Intercept", *X_train.columns])
print(compare.round(4))

prob = clf.predict_proba(features(test))[:, 1]
diff = np.abs(prob - sm.predict(test)).max()
print(f"Largest probability difference: {diff:.6f}")

default = LogisticRegression().fit(X_train, y_train)
print("Default C=1.0:", default.coef_[0].round(4))
