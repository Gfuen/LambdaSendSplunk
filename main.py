import boto3
import json
import requests

def lambda_handler(event, context):
    # Initialize Splunk Cloud endpoint and access token
    splunk_url = "REPLACE_ME"
    splunk_token = "REPLACE_ME"

    # Initialize the Splunk event collector
    splunk_headers = {"Authorization": "Splunk " + splunk_token}
    splunk_data = {"event": event}

    # Upload CloudTrail events to Splunk
    response = requests.post(splunk_url, headers=splunk_headers, data=json.dumps(splunk_data))

    # Check response
    if response.status_code == 200:
        print("Events uploaded successfully to Splunk.")
    else:
        print("Failed to upload events to Splunk. Status code:", response.status_code)

def get_cloudtrail_events():
    # Initialize AWS services
    cloudtrail = boto3.client('cloudtrail')

    # Get the last 10 events from CloudTrail
    response = cloudtrail.lookup_events(
        LookupAttributes=[
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'ConsoleLogin'
            },
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'AssumeRole'
            }
        ],
        MaxResults=10
    )

    # Extract relevant information from CloudTrail events
    events = []
    for event in response['Events']:
        events.append({
            'EventTime': str(event['EventTime']),
            'EventName': event['EventName'],
            'EventSource': event['EventSource'],
            'Username': event['Username'],
            'ResourceName': event['Resources'][0]['ResourceName']
        })

    return events

def lambda_handler(event, context):
    # Get CloudTrail events
    cloudtrail_events = get_cloudtrail_events()

    # Upload events to Splunk
    lambda_response = lambda_handler(cloudtrail_events, context)
    return lambda_response
