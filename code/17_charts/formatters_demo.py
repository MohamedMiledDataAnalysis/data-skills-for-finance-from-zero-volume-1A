from nbcharts import gbp, gbp_m, pct, thousands

for f in (gbp, gbp_m, pct, thousands):
    print(f(1234567.8, 0))
