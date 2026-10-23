# applied_monthly_pipeline.py — monthly cash-flow and arrears
# summary by customer segment, written as partitioned Parquet
import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-monthly-pipeline")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")


def read(name):
    return spark.read.csv(f"data/csv/{name}.csv",
                          header=True, inferSchema=True)


# ---- Step 1: read ------------------------------------------
txns = read("transactions")
accounts = read("accounts")
customers = read("customers")
loans = read("loans")
fx = read("fx_rates")
print("Step 1 read: txns", txns.count(), "| accounts",
      accounts.count(), "| customers", customers.count())
print("             loans", loans.count(), "| fx", fx.count())

# ---- Step 2: clean -----------------------------------------
txns_clean = (txns
              .dropDuplicates(["transaction_id"])
              .filter(F.col("amount").isNotNull())
              .withColumn("txn_month",
                          F.date_format("txn_date", "yyyy-MM")))
print("Step 2 clean: txns", txns_clean.count())

# Monthly average FX rate; a GBP row with rate 1.0 is added
# so that every transaction finds a rate in the join
fx_month = (fx
            .withColumn("txn_month",
                        F.date_format("rate_date", "yyyy-MM"))
            .groupBy("txn_month", "currency")
            .agg(F.avg("rate_per_gbp").alias("rate_per_gbp")))
gbp = (fx_month.select("txn_month").distinct()
       .withColumn("currency", F.lit("GBP"))
       .withColumn("rate_per_gbp", F.lit(1.0)))
fx_month = fx_month.unionByName(gbp)

# ---- Step 3: join ------------------------------------------
segments = customers.select("customer_id", "segment")
txn_seg = (txns_clean
           .join(F.broadcast(accounts.select("account_id",
                                             "customer_id")),
                 on="account_id", how="inner")
           .join(F.broadcast(segments), on="customer_id",
                 how="inner")
           .join(F.broadcast(fx_month),
                 on=["txn_month", "currency"], how="inner")
           .withColumn("amount_gbp",
                       F.col("amount") / F.col("rate_per_gbp")))
print("Step 3 join: txns", txn_seg.count())

# ---- Step 4: aggregate -------------------------------------
cash = (txn_seg.groupBy("txn_month", "segment")
        .agg(F.count("*").alias("txns"),
             F.round(F.sum(F.when(F.col("amount_gbp") > 0,
                                  F.col("amount_gbp"))
                           .otherwise(0)), 2).alias("inflow_gbp"),
             F.round(F.sum(F.when(F.col("amount_gbp") < 0,
                                  F.col("amount_gbp"))
                           .otherwise(0)), 2).alias("outflow_gbp"),
             F.round(F.sum("amount_gbp"), 2).alias("net_gbp")))

# Rates from unrounded sums; rounding is the last step
in_arrears_principal = F.when(F.col("status") != "Performing",
                              F.col("principal")).otherwise(0)
arrears = (loans.join(segments, on="customer_id")
           .groupBy("segment")
           .agg(F.sum("principal").alias("book"),
                F.sum(in_arrears_principal).alias("in_arrears"))
           .select("segment",
                   F.round(F.col("book") / 1e6, 2)
                   .alias("book_m"),
                   F.round(F.col("in_arrears") / 1e6, 2)
                   .alias("arrears_m"),
                   F.round(100 * F.col("in_arrears")
                           / F.col("book"), 2)
                   .alias("arrears_pct")))

summary = (cash.join(arrears, on="segment", how="left")
           .orderBy("txn_month", "segment"))
summary.select("txn_month", "segment", "txns", "net_gbp",
               "arrears_pct").show(6)

# ---- Step 5: write -----------------------------------------
(summary.write.mode("overwrite")
    .partitionBy("txn_month")
    .parquet("output/monthly_summary"))

# ---- Step 6: read back and check ---------------------------
back = spark.read.parquet("output/monthly_summary")
rows_ok = back.count() == summary.count()
txns_ok = (back.agg(F.sum("txns")).first()[0]
           == txns_clean.count())
print("Step 6 check: rows", back.count(),
      "| rows match:", rows_ok)
print("              transaction total matches:", txns_ok)

(back.groupBy("segment")
     .agg(F.sum("txns").alias("txns"),
          F.round(F.sum("net_gbp"), 2).alias("net_gbp_2025"),
          F.first("arrears_pct").alias("arrears_pct"))
     .orderBy("segment")
     .show())

spark.stop()
