# read_csv_schema.py — read loans.csv with an explicit schema
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    IntegerType, DateType,
)

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-read-schema")
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

loans = spark.read.csv(
    "data/csv/loans.csv", header=True, schema=loan_schema
)

loans.printSchema()
loans.select("loan_id", "product", "origination_date",
             "status").show(5, truncate=False)

spark.stop()
