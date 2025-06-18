from pyspark.sql import SparkSession

# Création de la session Spark avec Delta activée
spark = SparkSession.builder \
    .appName("ExportToCSV") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Chargement du Delta Lake
try:
    df = spark.read.format("delta").load("/opt/spark-data/delta/indemnites")
    df.printSchema()
    df.show()
except Exception as e:
    print("❌ ERREUR chargement Delta :", str(e))
    raise e

# Export CSV
try:
    df.write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv("/opt/spark-data/export/indemnites_csv")
    print(" Export CSV terminé.")
except Exception as e:
    print(" ERREUR export CSV :", str(e))
    raise e

spark.stop()
