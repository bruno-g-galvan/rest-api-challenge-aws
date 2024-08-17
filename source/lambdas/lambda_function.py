import pymysql
import os

# Database settings
rds_host = os.environ['RDS_HOST']
db_username = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']

connection = pymysql.connect(host=rds_host, user = db_username, passwd = db_password, db = db_name)

def lambda_handler(event, context):

    # Create a table
    cursor = connection.cursor()
    sql = """
    CREATE TABLE IF NOT EXISTS jobs (
        id INT NOT NULL AUTO_INCREMENT,
        job VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
    );
    """
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    for row in rows:
        print("{0} {1}".format(row[0], row[1]))


