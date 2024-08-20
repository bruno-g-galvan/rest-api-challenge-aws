import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, StringType

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Paths to the CSV files
s3_bucket = "s3://rest-api-test-data-landing-316328384763-us-east-1/tables/"
jobs_path = s3_bucket + "jobs.csv"
departments_path = s3_bucket + "departments.csv"
hired_employees_path = s3_bucket + "hired_employees.csv"

# Read all CSV files from the S3 bucket
departments_df = spark.read.format("csv").option("header", "false").option("delimiter", ',').load(departments_path)
jobs_df = spark.read.format("csv").option("header", "false").option("delimiter", ',').load(jobs_path)
hired_employees_df = spark.read.format("csv").option("header", "false").option("delimiter", ',').load(hired_employees_path)

# Renaming the columns of each DataFrame to meaningful names
departments_df = departments_df.toDF("id", "department")
jobs_df = jobs_df.toDF("id", "job")
hired_employees_df = hired_employees_df.toDF("id", "employee", "entry_date", "department_id", "job_id")

# Casting the columns to appropriate data types
# This ensures that the data is in the correct format before writing to the MySQL database
departments_df = departments_df.withColumn("id", col("id").cast(IntegerType())) \
                               .withColumn("department", col("department").cast(StringType()))
                               
jobs_df = jobs_df.withColumn("id", col("id").cast(IntegerType())) \
                 .withColumn("job", col("job").cast(StringType()))
                
hired_employees_df = hired_employees_df.withColumn("id", col("id").cast(IntegerType())) \
                                       .withColumn("employee", col("employee").cast(StringType())) \
                                       .withColumn("entry_date", col("entry_date").cast(StringType())) \
                                       .withColumn("department_id", col("department_id").cast(IntegerType())) \
                                       .withColumn("job_id", col("job_id").cast(IntegerType()))

# Writing the processed DataFrames to the MySQL database
# Each try block handles the writing operation for a specific table
try:
    departments_df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://rest-api-db-instance.cx486wyu2r7m.us-east-1.rds.amazonaws.com:3306/hr_management") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "departments") \
        .option("user", "admin") \
        .option("password", "adminadmin") \
        .mode("overwrite") \
        .save()
except Exception as e:
    print(f"Error writing departments table: {e}")

try:
    jobs_df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://rest-api-db-instance.cx486wyu2r7m.us-east-1.rds.amazonaws.com:3306/hr_management") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "jobs") \
        .option("user", "admin") \
        .option("password", "adminadmin") \
        .mode("overwrite") \
        .save()
except Exception as e:
    print(f"Error writing jobs table: {e}")

try:
    hired_employees_df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://rest-api-db-instance.cx486wyu2r7m.us-east-1.rds.amazonaws.com:3306/hr_management") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "hired_employees") \
        .option("user", "admin") \
        .option("password", "adminadmin") \
        .mode("overwrite") \
        .save()
except Exception as e:
    print(f"Error writing hired_employees table: {e}")

## In case we want to insert this df in batches, we can use this function and setting the batch_size
#def insert_in_batches(df: DataFrame, jdbc_url: str, table_name: str, batch_size: int):
#    # Calculate the number of partitions based on batch size
#    total_rows = df.count()
#    num_partitions = math.ceil(total_rows / batch_size)
#    
#    # Repartition the DataFrame
#    df = df.repartition(num_partitions)
#    
#    # Loop through each partition and write to MySQL
#    for i in range(num_partitions):
#        batch_df = df.filter((df['__partition_id'] == i))
#        batch_df.write \
#            .format("jdbc") \
#            .option("url", jdbc_url) \
#            .option("dbtable", table_name) \
#            .option("user", "admin") \
#            .option("password", "adminadmin") \
#            .option("batchsize", batch_size) \
#            .mode("append") \
#            .save()

#jdbc_url = "jdbc:mysql://rest-api-db-instance.cx486wyu2r7m.us-east-1.rds.amazonaws.com:3306/hr_management"
#table_name = "your_table"
#
## Insert in batches of 1000 rows for exmaple
#insert_in_batches(df, jdbc_url, table_name, 1000)

job.commit()

spark.stop()