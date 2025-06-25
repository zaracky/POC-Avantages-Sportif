from pyspark.sql import SparkSession
import os
import shutil

# Initialisation Spark
spark = SparkSession.builder \
    .appName("ExportToParquet") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

#  Lecture depuis le Delta Lake
try:
    df = spark.read.format("delta").load("/opt/spark-data/delta/activites_detaillees")
    df.printSchema()
    df.show()
except Exception as e:
    print(" ERREUR chargement Delta :", str(e))
    raise e

#  Répertoire temporaire pour l'écriture
temp_output_dir = "/opt/spark-data/export_parquet/activites_temp"

#  Nettoyage du dossier temporaire s’il existe
if os.path.exists(temp_output_dir):
    shutil.rmtree(temp_output_dir)

#  Export au format Parquet dans un seul fichier
try:
    df.coalesce(1).write \
        .mode("overwrite") \
        .parquet(temp_output_dir)
except Exception as e:
    print(" ERREUR export Parquet :", str(e))
    raise e

#  Renommer le fichier .parquet vers activites.parquet
try:
    final_output_path = "/opt/spark-data/export_parquet/activites.parquet"
    
    # Supprime l'ancien fichier s'il existe
    if os.path.exists(final_output_path):
        os.remove(final_output_path)

    # Recherche le fichier .parquet dans le dossier temporaire
    for file in os.listdir(temp_output_dir):
        if file.endswith(".parquet"):
            shutil.move(os.path.join(temp_output_dir, file), final_output_path)
            print(f" Fichier exporté : {final_output_path}")
            break

    # Nettoyage des fichiers inutiles
    shutil.rmtree(temp_output_dir)
except Exception as e:
    print(" ERREUR renommage fichier :", str(e))
    raise e

spark.stop()
