import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    url = 'https://example.com/api'  # Replace with your API endpoint
    
    try:
        logger.info('Making API request to %s', url)
        response = requests.get(url)
        logger.info('API response status: %d', response.status_code)

        if response.status_code == 200:
            data = response.json()
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Request was successful',
                    'data': data
                })
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({
                    'message': 'Request failed',
                    'error': response.text
                })
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