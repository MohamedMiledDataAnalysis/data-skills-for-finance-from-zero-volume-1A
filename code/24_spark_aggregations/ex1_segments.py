# ex1_segments.py — customers by segment
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex1-segments")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

customers = spark.read.csv("data/csv/customers.csv",
                           header=True, inferSchema=True)

(customers.groupBy("segment")
    .agg(F.count("*").alias("customers"),
         F.countDistinct("city").alias("cities"),
         F.round(F.avg("risk_rating"), 2).alias("avg_risk"),
         F.min("join_date").alias("first_joined"))
    .orderBy(F.col("customers").desc())
    .show())

spark.stop()
