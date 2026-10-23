# select_filter.py — choose columns, add columns, filter rows
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, round as spark_round

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-select-filter")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.csv(
    "data/csv/loans.csv", header=True, inferSchema=True
)

# 1. select: keep four columns, rename one with alias
print("1. select and alias")
loans.select(
    "loan_id",
    "product",
    col("principal"),
    col("interest_rate").alias("rate_pct"),
).show(3)

# 2. withColumn: annual interest in pounds
print("2. withColumn")
loans = loans.withColumn(
    "annual_interest",
    spark_round(col("principal") * col("interest_rate") / 100, 2),
)
loans.select("loan_id", "principal", "interest_rate",
             "annual_interest").show(3)

# 3. filter with a single condition
print("3. filter: principal over 500,000")
big = loans.filter(col("principal") > 500000)
print("Loans over £500,000:", big.count())

# 4. & means AND, | means OR; each condition in brackets
print("4. & and |")
risky_sme = loans.filter(
    (col("product") == "SME") & (col("status") != "Performing")
)
print("SME loans not performing:", risky_sme.count())
small_or_auto = loans.where(
    (col("principal") < 5000) | (col("product") == "Auto")
)
print("Under £5,000 or Auto:", small_or_auto.count())

# 5. isin: one of several values
print("5. isin")
arrears = loans.filter(
    col("status").isin("30+ DPD", "90+ DPD", "Default")
)
print("Loans in arrears or default:", arrears.count())

# 6. isNull / isNotNull: ltv is empty except for mortgages
print("6. isNull")
print("Loans without LTV:",
      loans.filter(col("ltv").isNull()).count())
print("Loans with LTV:",
      loans.filter(col("ltv").isNotNull()).count())

# 7. orderBy descending
print("7. orderBy")
arrears.orderBy(col("principal").desc()).select(
    "loan_id", "product", "principal", "status"
).show(5)

# 8. distinct values of one column
print("8. distinct")
loans.select("status").distinct().orderBy("status").show()

spark.stop()
