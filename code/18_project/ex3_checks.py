from monthly_report import load_loans


def check_loan_values(loans):
    bad_rate = ~loans["interest_rate"].between(0, 20)
    assert not bad_rate.any(), (
        f"rate outside 0-20% for {bad_rate.sum()} loan(s): "
        f"{loans.loc[bad_rate, 'loan_id'].tolist()}")
    mortgages = loans[loans["product"] == "Mortgage"]
    assert mortgages["ltv"].notna().all(), "Mortgage without LTV"
    over = mortgages["ltv"] > 100
    assert not over.any(), (
        f"{over.sum()} mortgages have an LTV above 100%")
    print("Loan value checks passed")


loans = load_loans()
check_loan_values(loans)

broken = loans.copy()
broken.loc[broken["loan_id"] == "L00007", "interest_rate"] = 45.0
try:
    check_loan_values(broken)
except AssertionError as error:
    print("Check failed:", error)
