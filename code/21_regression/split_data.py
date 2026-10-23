# split_data.py - build the training and test sets
from regdata import load_loans, split

data = load_loans()
train, test = split(data)
print("All loans:", len(data))
print("Training:", len(train), "Test:", len(test))
print("First test loans:", test["loan_id"].head(3).tolist())
for name, part in [("All", data), ("Training", train),
                   ("Test", test)]:
    count = part["non_performing"].sum()
    rate = part["non_performing"].mean() * 100
    print(f"{name}: {count} non-performing ({rate:.2f}%)")
