# applied_watch_list.py — build the credit risk watch list
# Mortgages with LTV above 80% or any loan in arrears/default,
# with annual interest and a risk band, saved as Parquet.
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, round as spark_round
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    IntegerType, DateType,
)

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-watch-list")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loan_schema = StructType([
    StructField("loan_id", StringType()),
    StructField("customer_id", StringType()),
    StructField("product", StringType()),
    StructField("principal", DoubleType()),
    StructField("interest_rate", DoubleType()),
    StructField("term_months", IntegerType()),
    StructField("origination_date", DateType()),
    StructField("status", StringType()),
    StructField("ltv", DoubleType()),
])

# Step 1: read with the explicit schema
loans = spark.read.csv("data/csv/loans.csv", header=True,
                       schema=loan_schema)
print("Step 1 - loans read:", loans.count())

# Step 2: keep the loans that meet either watch-list rule
high_ltv = (col("product") == "Mortgage") & (col("ltv") > 80)
in_arrears = col("status").isin("30+ DPD", "90+ DPD", "Default")
watch = loans.filter(high_ltv | in_arrears)
print("Step 2 - loans on the watch list:", watch.count())

# Step 3: add the reason, annual interest and a severity band
watch = (
    watch
    .withColumn("reason",
                when(in_arrears & high_ltv, "Arrears and LTV")
                .when(in_arrears, "Arrears")
                .otherwise("High LTV"))
    .withColumn("annual_interest",
                spark_round(col("principal")
                            * col("interest_rate") / 100, 2))
    .withColumn("severity",
                when(col("status") == "Default", "1 - Default")
                .when(col("status") == "90+ DPD", "2 - 90+ DPD")
                .when(col("status") == "30+ DPD", "3 - 30+ DPD")
                .otherwise("4 - Watch"))
)

# Step 4: sort: most severe first, largest principal first
watch = watch.orderBy(col("severity"), col("principal").desc())
watch.select("loan_id", "product", "principal", "status",
             "ltv", "reason").show(8)

# Step 5: count each reason
for reason in ["Arrears", "High LTV", "Arrears and LTV"]:
    n = watch.filter(col("reason") == reason).count()
    print(f"{reason:<16} {n:>4}")

# Step 6: save for the credit risk team and check the file
watch.write.mode("overwrite").parquet("output/watch_list")
check = spark.read.parquet("output/watch_list")
print("Step 6 - rows read back from Parquet:", check.count())

# Step 7: a five-line summary in pandas for the email
top = (check.orderBy(col("principal").desc())
       .select("loan_id", "product", "principal", "reason")
       .limit(5).toPandas())
print(top.to_string(index=False))

spark.stop()
