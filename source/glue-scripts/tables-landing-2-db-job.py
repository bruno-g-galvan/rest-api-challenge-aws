import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Define the S3 bucket and prefix (folder)
s3_path = "s3://rest-api-test-data-landing-316328384763-us-east-1/tables/departments.csv"

# Read all CSV files from the S3 bucket
df = spark.read.format("csv").option("header", "true").load(s3_path)

# Show the dataframe (Optional: for debugging)
df.show()

# Write the DataFrame to MySQL table in RDS
df.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://rest-api-db-instance.cx486wyu2r7m.us-east-1.rds.amazonaws.com:3306/hr_management") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "departments") \
    .option("user", "admin") \
    .option("password", "adminadmin") \
    .mode("append") \
    .save()

job.commit()