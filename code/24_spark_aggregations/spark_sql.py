# spark_sql.py — the same questions in SQL, run by Spark
import os
import sys

from pyspark.sql import SparkSession

# Make Spark's worker processes use this same Python
os.environ["PYSPARK_PYTHON"] = sys.executable

spark = (
    SparkSession.builder
    .appName("northbridge-spark-sql")
    .master("local[*]")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

for table in ["customers", "accounts", "loans"]:
    df = spark.read.csv(f"data/csv/{table}.csv",
                        header=True, inferSchema=True)
    df.createOrReplaceTempView(table)

# 1. Arrears by product (Chapter 5 used GROUP BY the same way)
spark.sql("""
    SELECT product,
           COUNT(*) AS loans,
           SUM(CASE WHEN status <> 'Performing'
                    THEN 1 ELSE 0 END) AS in_arrears,
           ROUND(100.0 * SUM(CASE WHEN status <> 'Performing'
                                  THEN 1 ELSE 0 END)
                 / COUNT(*), 2) AS arrears_pct
    FROM loans
    GROUP BY product
    ORDER BY arrears_pct DESC
""").show()

# 2. Join and HAVING: segments holding over £10m of loans
spark.sql("""
    SELECT c.segment,
           COUNT(l.loan_id) AS loans,
           ROUND(SUM(l.principal) / 1000000, 2) AS principal_m
    FROM loans AS l
    INNER JOIN customers AS c
        ON c.customer_id = l.customer_id
    GROUP BY c.segment
    HAVING SUM(l.principal) > 10000000
    ORDER BY principal_m DESC
""").show()

# 3. The five largest overdrafts (T-SQL would say TOP 5)
spark.sql("""
    SELECT account_id, customer_id, currency, balance
    FROM accounts
    WHERE balance < 0
    ORDER BY balance
    LIMIT 5
""").show()

spark.stop()
