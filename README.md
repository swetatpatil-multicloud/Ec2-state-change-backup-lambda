# Ec2-state-change-backup-lambda (Autosave EC2 Instance State Before Shutdown (Assignment number 18))

## Overview
This AWS Lambda function captures EC2 instance state-change events (e.g., running, stopping, stopped) via EventBridge and saves metadata to an S3 bucket. It ensures that every lifecycle transition of the instance is logged and backed up.

## Steps Followed

1. **Created EC2 Instance**
   - Launched an EC2 instance (`i-056a830ec0168c948`) in the `ap-south-1` region.
   - This instance was used to generate state-change events (start, stop).
     <img width="1564" height="860" alt="image" src="https://github.com/user-attachments/assets/a26b8394-8c7d-4f59-bf75-90b8f0f93197" />


2. **Created IAM Role**
   - Attached `AWSLambdaBasicExecutionRole` for CloudWatch logging.
   - Attached `AmazonEC2ReadOnlyAccess` for EC2 metadata.
   - Attached `AmazonS3FullAccess` for writing to S3.
<img width="1351" height="644" alt="image" src="https://github.com/user-attachments/assets/0a1b2662-1ddc-4a03-a6d4-1533456cbab4" />


3. **Created S3 Bucket**
   - Bucket name: `ec2backup-bucket1`
   - Used to store metadata JSON files under path:
     ```
     backups/<instance-id>/metadata.json
     ```
<img width="1658" height="695" alt="image" src="https://github.com/user-attachments/assets/75f852e1-ad85-4def-a85e-254ed76d9070" />


4. **Created EventBridge Rule**
   - Event pattern:
     ```json
     {
       "source": ["aws.ec2"],
       "detail-type": ["EC2 Instance State-change Notification"],
       "detail": {
         "instance-id": ["i-056a830ec0168c948"],
         "state": ["running", "stopping", "stopped"]
       }
     }
     ```
   - Target: Lambda function.
<img width="1602" height="779" alt="image" src="https://github.com/user-attachments/assets/f018185f-740d-4c50-8c88-4a660fac7d34" />


5. **Deployed Lambda Function**
   - Runtime: Python 3.14
   - Code in `lambda_function.py`
   - Handles both real EC2 events and console test events.
<img width="1547" height="826" alt="image" src="https://github.com/user-attachments/assets/bcf432ae-4e04-4ac7-a00b-dc53e864176c" />


6. **Tested Execution**
   - Console test event → returns `"state TEST"`.
   - Real EC2 stop/start → logs correct state (`running`, `stopping`, `stopped`) and saves metadata to S3.
<img width="1862" height="607" alt="image" src="https://github.com/user-attachments/assets/0e36a622-c788-4a93-8610-834ff59efbf4" />


7. **Verified Logs & S3**
   - CloudWatch Logs show event JSON and success messages.
   - S3 bucket contains `metadata.json` with instance details.
<img width="1565" height="708" alt="image" src="https://github.com/user-attachments/assets/d825080e-7b65-45c1-a581-973467a0a1b2" />


### Metadata.json under backup:
<img width="1482" height="654" alt="image" src="https://github.com/user-attachments/assets/d345672b-d4b8-463b-b7c7-69e3cd4918d4" />


### Log stream in CloudWatch generating logs:
<img width="1553" height="695" alt="image" src="https://github.com/user-attachments/assets/075555e1-3139-44b3-9359-555ce8be358d" />


## In Cloudwatch logs it’s showing that my instance is stopped:

<img width="1524" height="786" alt="image" src="https://github.com/user-attachments/assets/27d6033c-a58b-43bd-a3f5-a5cdd56a19a5" />


## Example Output
```json
{
  "InstanceId": "i-056a830ec0168c948",
  "State": "stopped",
  "EventTime": "2026-03-08T11:03:34Z"
}



