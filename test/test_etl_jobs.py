
def test_basic_etl_transformation():
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col

    spark = SparkSession.builder.master("local").appName("Test").getOrCreate()
    df = spark.createDataFrame([
        ("001", "residential", "Lima"),
        ("002", "commercial", "Cusco")
    ], ["customer_id", "customer_type", "city"])

    assert "customer_id" in df.columns
    assert df.count() == 2
