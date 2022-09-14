import os
from aws_cdk import (
    # Duration,
    aws_iam as iam,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_s3_notifications as s3_notify,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct


class S3TriggerLambdaProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # create new IAM group and use
        group = iam.Group(self, "CDKGroup")
        user = iam.User(self, "CDKUser")

        # Add IAM user to the group
        user.add_to_group(group)

        # Create S3 Bucket
        bucket = s3.Bucket(self, 'cdk-bucket')
        bucket.grant_read_write(user)

        # Create DynamoDB Table
        my_table = dynamodb.Table(self, "CdkFileTable",
            partition_key=dynamodb.Attribute(name="fileName", type=dynamodb.AttributeType.STRING))
        my_table.grant_read_write_data(user)

        # Create SNS Topic and add email subscription
        my_topic = sns.Topic(self, "cdk-topic")
        my_topic.add_subscription(subscriptions.EmailSubscription("<your-email-address>"))

        cwd = os.getcwd()
        # Create a lambda function
        lambda_func = _lambda.Function(self, 'lambda_listener',
                       runtime=_lambda.Runtime.PYTHON_3_8,
                       handler='lambda_listener.handler',
                       code=_lambda.Code.from_asset(os.path.join(cwd, "s3_trigger_lambda_project/lambda")),
                       environment={
                        'BUCKET_NAME': bucket.bucket_name,
                        'TABLE_NAME': my_table.table_name,
                        'TOPIC_ARN': my_topic.topic_arn
                        }
                    )
        
        # Lambda permissions for dynamodb and sns
        my_topic.grant_publish(lambda_func)
        my_table.grant_read_write_data(lambda_func)
        
        # Create trigger for Lambda function using suffix
        notification = s3_notify.LambdaDestination(lambda_func)
        notification.bind(self, bucket)

        # Add Create Event only for .jpg files
        bucket.add_object_created_notification(
           notification, s3.NotificationKeyFilter(suffix='.jpg'))
        
