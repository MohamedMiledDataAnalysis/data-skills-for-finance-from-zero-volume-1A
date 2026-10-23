# to_pandas.py — bring a small Spark result into pandas
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-to-pandas")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.csv(
    "data/csv/loans.csv", header=True, inferSchema=True
)

defaults = (
    loans.filter(col("status") == "Default")
    .select("loan_id", "product", "principal")
    .orderBy(col("principal").desc())
    .limit(5)
)

pdf = defaults.toPandas()
print(type(pdf))
print(pdf)
print("Total principal of top 5 defaults: £"
      f"{pdf['principal'].sum():,.2f}")

spark.stop()
