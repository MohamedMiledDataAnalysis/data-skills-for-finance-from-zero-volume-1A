# classifier_charts.py - box plot and ROC curve on the test set
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score, roc_curve

from regdata import load_loans, split

sys.path.append(str(Path(__file__).resolve().parents[1]
                    / "17_charts"))
from nbcharts import nb_style, add_titles, save_chart, PALETTE

train, test = split(load_loans())
model = smf.logit("non_performing ~ risk_rating + C(product)",
                  data=train).fit(disp=0)
test["prob"] = model.predict(test) * 100
print(test.groupby("non_performing")["prob"].median().round(2))
print(f"Highest probability: {test['prob'].max():.2f}%")

nb_style()
fig, ax = plt.subplots(figsize=(6, 3.2))
groups = [test.loc[test["non_performing"] == v, "prob"]
          for v in [0, 1]]
box = ax.boxplot(groups, orientation="horizontal", widths=0.5,
                 patch_artist=True,
                 medianprops={"color": PALETTE["gold"],
                              "linewidth": 2},
                 flierprops={"markersize": 4,
                             "markeredgecolor": PALETTE["slate"]})
for patch, colour in zip(box["boxes"], ["navy", "red"]):
    patch.set_facecolor(PALETTE[colour])
    patch.set_alpha(0.75)
ax.set_yticks([1, 2], ["Performing\n(273 loans)",
                       "Non-performing\n(27 loans)"])
ax.set_xlabel("Predicted probability of non-performing (%)")
ax.xaxis.set_major_formatter("{x:.0f}%")
ax.grid(axis="y", visible=False)
add_titles(ax, "Non-performing loans received higher "
               "probabilities")
save_chart(fig, "ch21_prob_box.png", "ch21-prob-box.png")

fpr, tpr, thresholds = roc_curve(test["non_performing"],
                                 test["prob"])
auc = roc_auc_score(test["non_performing"], test["prob"])
fig, ax = plt.subplots(figsize=(4.8, 4.2))
ax.plot(fpr * 100, tpr * 100, color=PALETTE["navy"],
        linewidth=2, label=f"Logistic model (AUC = {auc:.3f})")
ax.plot([0, 100], [0, 100], color=PALETTE["slate"],
        linestyle="--", linewidth=1.2,
        label="Random guess (AUC = 0.5)")
ax.set_xlabel("False alarm rate: performing loans flagged (%)")
ax.set_ylabel("Recall: non-performing loans caught (%)")
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.legend(loc="lower right")
add_titles(ax, "ROC curve on the 300 test loans")
save_chart(fig, "ch21_roc.png", "ch21-roc.png")
