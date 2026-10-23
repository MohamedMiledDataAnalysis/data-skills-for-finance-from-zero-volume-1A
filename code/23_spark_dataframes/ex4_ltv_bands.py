# ex4_ltv_bands.py — LTV bands for the mortgage book
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex4-ltv-bands")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.csv("data/csv/loans.csv",
                       header=True, inferSchema=True)

mortgages = (
    loans
    .filter(col("product") == "Mortgage")
    .withColumn("ltv_band",
                when(col("ltv") <= 60, "1: up to 60%")
                .when(col("ltv") <= 80, "2: 60-80%")
                .when(col("ltv") <= 90, "3: 80-90%")
                .otherwise("4: over 90%"))
)
mortgages.select("loan_id", "principal", "ltv",
                 "ltv_band").show(4)

bands = [r["ltv_band"] for r in
         mortgages.select("ltv_band").distinct()
         .orderBy("ltv_band").collect()]
for band in bands:
    n = mortgages.filter(col("ltv_band") == band).count()
    print(f"{band:<14} {n:>4} mortgages")

spark.stop()
