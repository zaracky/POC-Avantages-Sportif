from pyspark.sql import SparkSession

# Création d'une session Spark avec Delta Lake activé
spark = SparkSession.builder \
    .appName("WriteToDeltaLake") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Lecture depuis PostgreSQL
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/sportdb") \
    .option("dbtable", "activites_detaillees") \
    .option("user", "user") \
    .option("password", "password") \
    .load()


# Sauvegarde au format Delta avec gestion du schéma
df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .option("mergeSchema", "true") \
    .save("/opt/spark-data/delta/activites_detaillees")

spark.stop()
