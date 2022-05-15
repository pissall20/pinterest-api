import pandas as pd
import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf
from pyspark.sql.types import TimestampType


def create_spark_session(master_url, packages=None):
    """
    Creates a local spark session
    :param master_url: IP address of the cluster you want to submit the job to or local with all cores
    :param packages: Any external packages if needed, only when called. This variable could be a string of the package
        specification or a list of package specifications.
    :return: spark session object
    """
    if packages:
        packages = ",".join(packages) if isinstance(packages, list) else packages
        spark = (
            SparkSession.builder.master(master_url)
            .config("spark.io.compression.codec", "snappy")
            .config("spark.ui.enabled", "false")
            .config("spark.jars.packages", packages)
            .getOrCreate()
        )
    else:
        spark = (
            SparkSession.builder.master(master_url)
            .config("spark.io.compression.codec", "snappy")
            .config("spark.ui.enabled", "false")
            .getOrCreate()
        )

    return spark


def connect_to_sql(
    spark_master_url, jdbc_hostname, jdbc_port, database, data_table, username, password
):
    spark = create_spark_session(spark_master_url)
    jdbc_url = "jdbc:mysql://{0}:{1}/{2}".format(jdbc_hostname, jdbc_port, database)

    connection_details = {
        "user": username,
        "password": password,
        "driver": "com.mysql.cj.jdbc.Driver",
    }

    df = spark.read.jdbc(url=jdbc_url, table=data_table, properties=connection_details)
    return df


def spark_cassandra_connector(
    spark_master_url, connection_host, table_name, key_space, cassandra_package=None
):
    # A cassandra connector is needed
    needed_spark_package = (
        cassandra_package
        if cassandra_package
        else "com.datastax.spark:spark-cassandra-connector_2.11:2.4.0"
    )

    spark = create_spark_session(
        master_url=spark_master_url, packages=needed_spark_package
    )

    spark.conf.set("spark.cassandra.connection.host", str(connection_host))
    data = spark.read.format("org.apache.spark.sql.cassandra").load(
        keyspace=key_space, table=table_name
    )
    return data
