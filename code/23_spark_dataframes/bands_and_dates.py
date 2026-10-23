# bands_and_dates.py — when/otherwise, cast and to_date
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, to_date, year

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-bands")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

# Read every column as text, as some source systems deliver it
raw = spark.read.csv("data/csv/loans.csv", header=True)
raw.select("principal", "interest_rate",
           "origination_date").printSchema()

loans = (
    raw
    .withColumn("principal", col("principal").cast("double"))
    .withColumn("interest_rate",
                col("interest_rate").cast("double"))
    .withColumn("term_months", col("term_months").cast("int"))
    .withColumn("origination_date",
                to_date(col("origination_date"), "yyyy-MM-dd"))
)
loans.select("principal", "interest_rate", "term_months",
             "origination_date").printSchema()

loans = loans.withColumn(
    "rate_band",
    when(col("interest_rate") < 4, "Low (<4%)")
    .when(col("interest_rate") < 7, "Medium (4-7%)")
    .otherwise("High (7%+)"),
).withColumn("orig_year", year(col("origination_date")))

loans.select("loan_id", "interest_rate", "rate_band",
             "origination_date", "orig_year").show(6)

for band in ["Low (<4%)", "Medium (4-7%)", "High (7%+)"]:
    n = loans.filter(col("rate_band") == band).count()
    print(f"{band:<14} {n:>5} loans")

spark.stop()
