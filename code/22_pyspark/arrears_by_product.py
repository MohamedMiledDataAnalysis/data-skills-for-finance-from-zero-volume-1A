# arrears_by_product.py - loans not performing, by product
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("Northbridge arrears")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.csv(
    "data/csv/loans.csv", header=True, inferSchema=True
)
summary = (
    loans.filter(F.col("status") != "Performing")
    .groupBy("product")
    .agg(
        F.count("*").alias("loans"),
        F.round(F.sum("principal"), 2).alias("principal_gbp"),
    )
    .orderBy("product")
)
summary.show()
spark.stop()
