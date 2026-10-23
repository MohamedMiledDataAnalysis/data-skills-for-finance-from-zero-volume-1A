# s_curve.py - the logistic function turns any number into 0 to 1
import numpy as np

for z in [-6, -4, -2, 0, 2, 4, 6]:
    p = 1 / (1 + np.exp(-z))
    print(f"log-odds {z:>3} -> probability {p:.4f}")
