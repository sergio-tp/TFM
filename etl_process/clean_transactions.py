from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def main():
    try:
        # First of all, we create and configure the Spark session using Apache Spark.
        spark = SparkSession.builder \
            .appName("CleaningTransactions") \
            .master("local[*]") \
            .getOrCreate()
        
        spark.sparkContext.setLogLevel("ERROR")

        # Once the dataset has been loaded, we proceed with its cleaning and preparation for the ETL process.
        df = spark.read \
            .option("header", True) \
            .option("inferSchema", True) \
            .option("sep", ";") \
            .csv("../datasets/dataset_transactions.csv", header=True, inferSchema=True)

        # First of all, we select the columns of interest and we rename them.
        df = df.drop("CODCOMUNIDAD", "CODPROVINCIA")
        
        df = df.withColumnRenamed("COMUNIDAD", "Region") \
            .withColumnRenamed("PROVINCIA", "City") \
            .withColumnRenamed("Año", "Year") \
            .withColumnRenamed("Numero_Transacciones", "Total_Transactions") \
            .withColumnRenamed("Valor_Transacciones", "Total_Price") \
            .withColumnRenamed("Trimestre", "Quarter")

        # Now we can see that some columns are not in the format we need, so we will transform them.
        df = df.withColumn("Region",
            F.when(
                F.col("Region").contains(","),
                F.concat_ws(
                    " ",
                    F.trim(F.element_at(F.split(F.col("Region"), ","), 2)),
                    F.trim(F.element_at(F.split(F.col("Region"), ","), 1))
                )
            ).otherwise(F.col("Region"))
        )

        df = df.withColumn(
            "Region",
            F.when(F.col("Region") == "Castilla-La Mancha", "Castilla - La Mancha")
             .otherwise(F.col("Region"))
        )

        df = df.withColumn("City",
            F.when(
                F.col("City").contains(","),
                F.concat_ws(
                    " ",
                    F.trim(F.element_at(F.split(F.col("City"), ","), 2)),
                    F.trim(F.element_at(F.split(F.col("City"), ","), 1))
                )
            ).otherwise(F.col("City"))
        )

        df = df.withColumn(
            "Regime",
            F.when(F.col("Tipo").isin("Protegida Nueva", "Protegida Segunda Mano"), "Protegida")
            .otherwise("Libre")
        )

        df = df.withColumn(
            "Condition",
            F.when(F.col("Tipo").isin("Protegida Nueva", "Nueva"), "Nueva")
             .otherwise("Segunda mano")
        )

        df = df.drop("Tipo")

        df.coalesce(1).write \
            .mode("append") \
            .option("header", True) \
            .csv("../datasets_def/transactions_clean")

        spark.stop()
        print("Process executed successfully.")
        
    except Exception as e:
        print(f"Execution error: {e}")

if __name__ == "__main__":
    main()