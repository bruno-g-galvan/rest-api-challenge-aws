import json
import requests

def lambda_handler(event, context):
    url = 'https://kuwvvh3ktd.execute-api.us-east-1.amazonaws.com/prod/status'  # Replace with your API endpoint
    
    try:
        response = requests.get(url)  # You can use requests.post() for POST requests

        if response.status_code == 200:
            # Process the response as needed
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
        # Handle any exceptions that occur during the request
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'An error occurred',
                'error': str(e)
            })
        }