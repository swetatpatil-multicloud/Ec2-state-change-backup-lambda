import boto3
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # Handle both test events and real EC2 events
    if "detail" in event:
        instance_id = event['detail']['instance-id']
        state = event['detail']['state']
        event_time = event['time']
    else:
        # Fallback for console test events
        instance_id = "i-056a830ec0168c948"
        state = "TEST"
        event_time = "N/A"

    # Build metadata dictionary
    metadata = {
        "InstanceId": instance_id,
        "State": state,
        "EventTime": event_time
    }

    # Save metadata to S3 bucket
    s3.put_object(
        Bucket="ec2backup-bucket1",
        Key=f"backups/{instance_id}/metadata.json",
        Body=json.dumps(metadata, indent=4, default=str)  # FIX applied here
    )

    print(f"Saved state of {instance_id} to S3 bucket ec2backup-bucket1")

    # Explicit return so Lambda console shows a result
    return {
        "statusCode": 200,
        "body": f"Metadata for {instance_id} with state {state} saved to S3."
    }
