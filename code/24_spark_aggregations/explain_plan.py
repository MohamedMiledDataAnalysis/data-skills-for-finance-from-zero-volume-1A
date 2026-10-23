# explain_plan.py — ask Spark how it will run a query
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-explain")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.parquet("output/loans_parquet")

summary = (loans
           .filter(F.col("status") != "Performing")
           .groupBy("product")
           .agg(F.sum("principal").alias("arrears_principal")))

summary.explain()

spark.stop()
