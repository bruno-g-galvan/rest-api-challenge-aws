import json
import logging
import requests
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    status_url = 'https://kuwvvh3ktd.execute-api.us-east-1.amazonaws.com/prod/status'
    hired_employees_2021_url = 'https://kuwvvh3ktd.execute-api.us-east-1.amazonaws.com/prod/hired_employees_2021'
    hired_employees_2021_quarters_url = 'https://kuwvvh3ktd.execute-api.us-east-1.amazonaws.com/prod/hired_employees_2021_quarters'
    
    results = {}

    try:
        # Check the /status URL
        logger.info('Making API request to %s', status_url)
        status_response = requests.get(status_url)
        logger.info('Status API response status: %d', status_response.status_code)
        results['status'] = {
            'statusCode': status_response.status_code,
            'body': status_response.text
        }

        if status_response.status_code != 200:
            logger.error('Status API request failed with status code: %d', status_response.status_code)
            return {
                'statusCode': status_response.status_code,
                'body': json.dumps({
                    'message': 'Status request failed',
                    'error': status_response.text
                })
            }

        # Check the /hired_employees_2021 URL
        logger.info('Making API request to %s', hired_employees_2021_url)
        employees_response = requests.get(hired_employees_2021_url)
        logger.info('Hired_employees_2021 URL response status: %d', employees_response.status_code)
        results['hired_employees_2021'] = {
            'statusCode': employees_response.status_code,
            'body': employees_response.text
        }

        if employees_response.status_code != 200:
            logger.error('Hired_employees_2021 URL request failed with status code: %d', employees_response.status_code)
            return {
                'statusCode': employees_response.status_code,
                'body': json.dumps({
                    'message': 'Hired_employees_2021 URL request failed',
                    'error': employees_response.text
                })
            }

        # Check the /hired_employees_2021_quarters URL
        logger.info('Making API request to %s', hired_employees_2021_quarters_url)
        quarters_response = requests.get(hired_employees_2021_quarters_url)
        logger.info('Hired_employees_2021_quarters URL response status: %d', quarters_response.status_code)
        results['hired_employees_2021_quarters'] = {
            'statusCode': quarters_response.status_code,
            'body': quarters_response.text
        }

        if quarters_response.status_code != 200:
            logger.error('Hired_employees_2021_quarters URL request failed with status code: %d', quarters_response.status_code)
            return {
                'statusCode': quarters_response.status_code,
                'body': json.dumps({
                    'message': 'Hired_employees_2021_quarters URL request failed',
                    'error': quarters_response.text
                })
            }

        return {
            'statusCode': 200,
            'body': json.dumps(results)
        }

    except requests.RequestException as e:
        logger.error('Request exception: %s', str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'An error occurred',
                'error': str(e)
            })
        }