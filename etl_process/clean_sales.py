from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def main():
    try:
        # First of all, we create and configure the Spark session using Apache Spark.
        spark = SparkSession.builder \
            .appName("CleaningSales") \
            .master("local[8]") \
            .getOrCreate()
        
        spark.sparkContext.setLogLevel("ERROR")

        # Once the dataset has been loaded, we proceed with its cleaning and preparation for the ETL process.
        df = spark.read \
            .option("header", True) \
            .option("inferSchema", True) \
            .option("sep", ";") \
            .csv("../datasets/dataset_sales.csv")

        # First of all, we select the columns of interest and we rename them.
        df = df.drop("Total Nacional")
        
        df = df.withColumnRenamed("Comunidades y Ciudades Autónomas", "Region") \
            .withColumnRenamed("Provincias", "City") \
            .withColumnRenamed("Periodo", "Period") \
            .withColumnRenamed("Régimen y estado", "Regime_Condition")

        # Now we can see that some columns are not in the format we need, so we will transform them.
        df = df.withColumn("Region", F.trim(F.regexp_replace(F.col("Region"), r"^\d+\s+", "")))
        
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

        df = df.dropna(subset=["Region", "City"])
        
        df = df.withColumn("City", F.trim(F.regexp_replace(F.col("City"), r"^\d+\s+", "")))
        
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

        # Let's see the different values we can obtain in "Regime_Condition" column.
        df = df.withColumn(
            "Regime",
            F.when(F.col("Regime_Condition") == "Vivienda protegida", "Protegida")
             .when(F.col("Regime_Condition") == "Vivienda libre", "Libre")
        )
        
        df = df.withColumn(
            "Condition",
            F.when(F.col("Regime_Condition") == "Vivienda nueva", "Nueva")
             .when(F.col("Regime_Condition") == "Vivienda usada", "Segunda mano")
        )
        
        df = df.drop("Regime_Condition").dropna(subset=["Regime", "Condition"], how="all")

        # Finally, the date column will be transformed by splitting its information into two separate fields, year and month, in order to facilitate its subsequent analysis.
        df = df.withColumn("Year", F.substring(F.col("Period"), 1, 4).cast("int")) \
               .withColumn("Month", F.substring(F.col("Period"), 6, 2).cast("int"))
        
        df = df.drop("Period")

        df.coalesce(1).write \
            .mode("overwrite") \
            .option("header", True) \
            .csv("../datasets_def/sales_clean")

        spark.stop()
        print("Process executed successfully.")
        
    except Exception as e:
        print(f"Execution error: {e}")

if __name__ == "__main__":
    main()