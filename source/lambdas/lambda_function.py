import pymysql
import os

# Database settings
rds_host = os.environ['RDS_HOST']
db_username = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

def lambda_handler(event, context):
    try:
        # Establish the connection
        connection = pymysql.connect(
            host=rds_host,
            user=db_username,
            password=db_password,
            db=db_name,
            connect_timeout=5
        )
        
        # Create a table
        with connection.cursor() as cursor:
            create_table_sql = """
            CREATE DATABASE hr_management;
            CREATE TABLE IF NOT EXISTS jobs (
                id INT NOT NULL AUTO_INCREMENT,
                job VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
            );
            """
            cursor.execute(create_table_sql)
            connection.commit()  # Commit the transaction if needed

        return {
            'statusCode': 200,
            'body': 'Table created successfully.'
        }
    except pymysql.MySQLError as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
    finally:
        if connection:
            connection.close()

