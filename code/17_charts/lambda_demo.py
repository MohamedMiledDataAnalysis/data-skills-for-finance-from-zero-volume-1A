def gbp_label(x, pos):
    return f"£{x:,.0f}"


gbp_label_short = lambda x, pos: f"£{x:,.0f}"

print(gbp_label(2500000, 0))
print(gbp_label_short(2500000, 0))
