# types_and_conversion.py - what kind of value is this?
print(type(250000))
print(type(4.5))
print(type("4.5"))
print(type(True))

text_rate = "4.5"          # a rate read from a file is text
rate = float(text_rate)    # convert text to a decimal number
print(rate * 2)

term = int("300")          # convert text to a whole number
print(term // 12)

print(int(7.99))           # int() drops the fraction
print(round(7.99))         # round() rounds to the nearest
print(round(1234.5678, 2))
print(str(250000) + " GBP")
