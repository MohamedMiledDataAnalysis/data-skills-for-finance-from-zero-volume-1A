# aggregations.py — groupBy and agg on the loan book
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-aggregations")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.csv("data/csv/loans.csv",
                       header=True, inferSchema=True)

# 1. One number for the whole book
loans.agg(
    F.count("*").alias("loans"),
    F.round(F.sum("principal") / 1e6, 2).alias("principal_m"),
    F.round(F.avg("interest_rate"), 2).alias("avg_rate"),
    F.countDistinct("customer_id").alias("borrowers"),
).show()

# 2. One row per product
by_product = (
    loans.groupBy("product")
    .agg(
        F.count("*").alias("loans"),
        F.round(F.sum("principal") / 1e6, 2).alias("principal_m"),
        F.round(F.avg("principal"), 0).alias("avg_principal"),
        F.round(F.avg("interest_rate"), 2).alias("avg_rate"),
        F.round(
            F.sum(F.col("principal") * F.col("interest_rate"))
            / F.sum("principal"), 2
        ).alias("wavg_rate"),
    )
    .orderBy(F.col("principal_m").desc())
)
by_product.show()

# 3. Two grouping columns, then a filter on the result
by_prod_status = (
    loans.groupBy("product", "status")
    .agg(F.count("*").alias("loans"))
    .filter(F.col("status") != "Performing")
    .orderBy("product", "status")
)
by_prod_status.show()

spark.stop()
