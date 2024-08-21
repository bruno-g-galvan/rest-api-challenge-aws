import json
import requests

def lambda_handler(event, context):
    # List of URLs to check
    urls = {
        'status': 'https://kuwvvh3ktd.execute-api.us-east-1.amazonaws.com/prod/status',
        'hired_employees_2021': 'https://kuwvvh3ktd.execute-api.us-east-1.amazonaws.com/prod/hired_employees_2021',
        'hired_employees_2021_quarters': 'https://kuwvvh3ktd.execute-api.us-east-1.amazonaws.com/prod/hired_employees_2021_quarters'
    }
    
    for name, url in urls.items():
        try:
            # Make the API request
            response = requests.get(url)
            
            # Check if the response status code is 200
            if response.status_code != 200:
                raise Exception(f"{name} API request failed with status code {response.status_code}")
        
        except requests.RequestException as e:
            # Log the error and raise an exception to fail the Lambda function
            raise Exception(f"RequestException for {name}: {e}")
    
    # If all checks pass, return success
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'All API requests were successful'
        })
    }