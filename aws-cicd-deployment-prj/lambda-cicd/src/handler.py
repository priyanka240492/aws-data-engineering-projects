import json

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Lambda via CloudFormation CI/CD!",
            "input": event
        }) #json.dumps() converts the Python dictionary to a JSON string  
    }