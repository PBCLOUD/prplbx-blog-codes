import boto3
import os
import json

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')


def handler(event, context):
    
    bucket_name = (os.environ['BUCKET_NAME'])
    table_name = (os.environ['TABLE_NAME'])
    topic_arn = (os.environ['TOPIC_ARN'])

    key = event['Records'][0]['s3']['object']['key']

    try:
        # Log the event
        print("[lambda_listener] New file with name {} created in bucket {}".format(
            key, bucket_name))
        
        # Create sns message
        notification = "New file with name {} created in bucket {}".format(key, bucket_name)
        
        # Put fileName in dynamodb table
        dynamodb.put_item(
            TableName= table_name, 
            Item={
                'fileName':{'S': key}
            }
        )

        # publish sns message
        sns.publish (
            TargetArn = topic_arn,
            Message = json.dumps({'default': notification}),
            MessageStructure = 'json'
        )
        
        response = {
            'status': 'success', 
            'code': 201
        }

        return response

    except Exception as e:
        print(e)
        print("[Error] :: Error processing file {} from bucket {}. ".format(
            key, bucket_name))
        raise e
