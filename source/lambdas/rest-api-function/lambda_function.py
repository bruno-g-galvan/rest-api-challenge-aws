import pymysql
import os
import json
import boto3
from botocore.exceptions import ClientError

# Database settings
rds_host = os.environ['RDS_HOST']
db_name = os.environ['DB_NAME']

#connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)

status_check_path = '/status'
jobs_path = '/jobs'
departments_path = '/departments'
hired_employees_2021_quarters_path = '/hired_employees_2021_quarters'
hired_employees_2021_path = '/hired_employees_2021'

# Create a Secrets Manager client
client = boto3.client('secretsmanager', region_name='us-west-1')

values = client.get_secret_value(SecretId=os.environ['SECRET_NAME'])

# Parse the secret
secret = values['SecretString']
secret_dict = json.loads(secret)

db_username = secret_dict.get('username')
db_password = secret_dict.get('password')


def lambda_handler(event, context):
    print('Request event: ', event)
    response = {} #json.dumps(event)
    http_method = event.get('httpMethod')
    path = event.get('path')

    try:
        if http_method == 'GET':
            if path == status_check_path:
                response = ['Service is operational']
            elif path == jobs_path:
                response = get_jobs()
            elif path == departments_path:
                response = get_departments()
            elif path == hired_employees_2021_path:
                response = hired_employees_2021()
            elif path == hired_employees_2021_quarters_path:
                response = hired_employees_2021_quarters()
        elif http_method == 'POST':
            if path == jobs_path:
                response = save_jobs(json.loads(event['body']))
            elif path == departments_path:
                response = save_departments(json.loads(event['body']))
        elif http_method == 'DELETE':
            if path == jobs_path:
                response = delete_jobs(json.loads(event['body']))
            elif path == departments_path:
                response = delete_departments(json.loads(event['body']))
            
        else:
            response = {'error': 'Incorrect path.'}
    
    except Exception as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
   
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }
    
def get_jobs():
    try:
        connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)
        with connection.cursor() as cursor:
            
            #Select the value
            select_sql = """
            SELECT * FROM jobs;
            """
            
            cursor.execute(select_sql)
            #result = cursor.fetchall()
            
            result = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
            
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': result
        }
        
    except ClientError as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    finally:
        if connection:
            connection.close()

def get_departments():
    try:
        connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)
        with connection.cursor() as cursor:
            
            #Select the value
            select_sql = """
            SELECT * FROM departments;
            """
            
            cursor.execute(select_sql)
            #result = cursor.fetchall()
            
            result = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
            
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': result
        }
        
    except ClientError as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    finally:
        if connection:
            connection.close()

def save_jobs(request_body):
    try:
        connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)
        # Extract the value associated with the "job" key
        job_value = request_body["job"]
        
        try:
            with connection.cursor() as cursor:
                # SQL query to insert JSON data into the table
                sql = "INSERT INTO jobs (job) VALUES (%s)"
                cursor.execute(sql, (job_value,))
            
            # Commit the transaction
            connection.commit()
        
        finally:
            connection.close()
            
    except ClientError as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
        
def save_departments(request_body):
    try:
        connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)
        # Extract the value associated with the "job" key
        id_value = request_body["id"]
        department_value = request_body["department"]
        
        try:
            with connection.cursor() as cursor:
                # SQL query to insert JSON data into the table
                sql = "INSERT INTO departments (id, department) VALUES (%s, %s)"
                cursor.execute(sql, (id_value,department_value))
            
            # Commit the transaction
            connection.commit()
        
        finally:
            connection.close()
            
    except ClientError as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def delete_jobs(request_body):
    try:
        connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)
        # Extract the value associated with the "job" key
        id_value = request_body["id"]
        
        try:
            with connection.cursor() as cursor:
                # SQL query to insert JSON data into the table
                sql = "DELETE FROM jobs WHERE id = %s"
                cursor.execute(sql, (id_value,))
            
            # Commit the transaction
            connection.commit()
        
        finally:
            connection.close()
            
    except ClientError as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def delete_departments(request_body):
    try:
        connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)
        # Extract the value associated with the "job" key
        id_value = request_body["id"]
        
        try:
            with connection.cursor() as cursor:
                # SQL query to insert JSON data into the table
                sql = "DELETE FROM departments WHERE id = %s"
                cursor.execute(sql, (id_value,))
            
            # Commit the transaction
            connection.commit()
        
        finally:
            connection.close()
            
    except ClientError as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def hired_employees_2021():
    try:
        connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)
        with connection.cursor() as cursor:
            #Select the value
            select_sql = """
                        SELECT
                            id,
                            department,
                            hired
                        FROM (
                            SELECT
                                id,
                                department,
                                count(employee) as hired
                            FROM (
                                SELECT
                                    departments.id as id,
                                    departments.department as department,
                                    hired_employees.employee,
                                    YEAR(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_year,
                                    QUARTER(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_quarter
                                FROM departments
                                LEFT JOIN hired_employees
                                ON departments.id = hired_employees.department_id) AS subquery
                                WHERE entry_year = 2021
                                GROUP BY id, department
                            ) AS subquery2
                        WHERE hired > (
                            SELECT 
                                AVG(hired)
                            FROM (
                                    SELECT
                                        departments.id as id,
                                        departments.department as department,
                                        count(hired_employees.employee) as hired
                                    FROM departments
                                    LEFT JOIN hired_employees
                                    ON departments.id = hired_employees.department_id
                                    WHERE YEAR(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) = 2021
                                    GROUP BY id, department
                                    ) AS subquery
                                )
                        ORDER BY hired DESC;
                        """
            cursor.execute(select_sql)
            result = cursor.fetchall()
            lst = []
            for row in result:
                job = {'id':row[0],'department':row[1],'hired':row[2]}
                lst.append(job)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': lst
        }
        
    except ClientError as e:
        print('Error:', e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    finally:
        if connection:
            connection.close()

def hired_employees_2021_quarters():
    try:
        connection = pymysql.connect(host = rds_host, user = db_username, passwd = db_password, db=db_name)
        with connection.cursor() as cursor:
            #Select the value
            select_sql = """
                        SELECT 
                        	department,
                        	job,
                            COUNT(CASE WHEN entry_quarter = 1 THEN 1 END) AS Q1,
                            COUNT(CASE WHEN entry_quarter = 2 THEN 1 END) AS Q2,
                            COUNT(CASE WHEN entry_quarter = 3 THEN 1 END) AS Q3,
                            COUNT(CASE WHEN entry_quarter = 4 THEN 1 END) AS Q4
                        FROM (
                        	SELECT
                        		hired_employees.id as id,
                        		hired_employees.employee as employee,
                        		YEAR(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_year,
                                QUARTER(STR_TO_DATE(hired_employees.entry_date, '%Y-%m-%dT%H:%i:%s')) as entry_quarter,
                        		hired_employees.department_id as department_id,
                        		hired_employees.job_id as job_id,
                        		departments.department as department,
                        		jobs.job as job
                        	FROM hired_employees 
                        	LEFT JOIN departments
                        	ON departments.id = hired_employees.department_id
                        	LEFT JOIN jobs
                        	ON jobs.id = hired_employees.job_id
                        ) AS subquery
                        WHERE entry_year = 2021
                        GROUP BY job, department
                        ORDER BY count(id) DESC;
                        """
            cursor.execute(select_sql)
            result = cursor.fetchall()
            lst = []  # List to hold the dictionaries
            for row in result:
                job = {
                    'department': row[0].replace('\\', '') if row[0] is not None else '',
                    'job': row[1].replace('\\', '') if row[1] is not None else '',
                    'Q1': row[2] if row[2] is not None else 0,
                    'Q2': row[3] if row[3] is not None else 0,
                    'Q3': row[4] if row[4] is not None else 0,
                    'Q4': row[5] if row[5] is not None else 0
                }
                lst.append(job)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': lst
        }
        
    except ClientError as e:
        print('Error:', e)

def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }