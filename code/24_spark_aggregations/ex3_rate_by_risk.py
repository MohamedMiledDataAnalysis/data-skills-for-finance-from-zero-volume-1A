# ex3_rate_by_risk.py — weighted average rate and arrears
# by customer risk rating
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("ex3-rate-by-risk")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

loans = spark.read.csv("data/csv/loans.csv",
                       header=True, inferSchema=True)
customers = spark.read.csv("data/csv/customers.csv",
                           header=True, inferSchema=True)

joined = loans.join(
    F.broadcast(customers.select("customer_id", "risk_rating")),
    on="customer_id", how="left",
)
print("Loans after left join:", joined.count())
print("Loans with no risk rating:",
      joined.filter(F.col("risk_rating").isNull()).count())

(joined.groupBy("risk_rating")
    .agg(F.count("*").alias("loans"),
         F.round(F.sum(F.col("principal") * F.col("interest_rate"))
                 / F.sum("principal"), 2).alias("wavg_rate"),
         F.round(100 * F.avg(F.when(F.col("status")
                                    != "Performing", 1)
                             .otherwise(0)), 2)
          .alias("arrears_pct"))
    .orderBy("risk_rating")
    .show())

spark.stop()
