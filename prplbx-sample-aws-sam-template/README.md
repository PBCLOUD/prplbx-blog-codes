# SAM DEMO APP

This AWS SAM demo app consists of S3-triggered Lambda and SNS Topic. When an object is put in the AWS S3 bucket, the AWS Lambda function will be triggered, and writes the name of the object to the AWS DynamoDB table and then notify the action to us via email. There are source code and supported files for this app.

## Pre-Requirements
- AWS CLI
- Homebrew (For Linux and macOS)
- AWS SAM CLI (1.13.0 or later)
- Nodejs


## Usage

- sam init
  
  It initializes a new serverless app
  
- sam build 

  It builds the application and makes installation dependencies and packaging according to the runtime of the relevant project. 

- sam deploy --guided 

  It packages and uploads the application artifacts to the S3 bucket, then deploys the application using AWS CloudFormation.


## Testing

To test the application, you need to upload a file to the S3 bucket from AWS Console or CLI. Then you need to check your email. There should be an email like "Object is added". Besides, check the DynamoDB table whether the object name is written.

