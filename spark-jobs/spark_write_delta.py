from pyspark.sql import SparkSession

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

# Sélection explicite des colonnes (évite les doublons inattendus)
df_clean = df.select(
    "id_salarie", "nom", "prenom", "date_activite", "type_activite",
    "distance_m", "duree_s", "commentaire", "est_eligible", "montant_rembourse"
)

#  Écriture en mode overwrite complet
df_clean.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save("/opt/spark-data/delta/activites_detaillees")

spark.stop()
