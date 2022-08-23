const AWS = require("aws-sdk");
const s3 = new AWS.S3({
   region: 'us-east-1'
});
const dynamodb = new AWS.DynamoDB.DocumentClient({
   apiVersion: '2012-08-10',
   region: 'us-east-1'
 });
const sns = new AWS.SNS({apiVersion: '2012-11-05'})

exports.handler = async function index(event, context) {
   try {

    console.log('event:' + JSON.stringify(event));
    const tableName = process.env.SAMPLE_TABLE;
    const params = {
        TableName: tableName,
        Item: {
            objectname: event.Records[0].s3.object.key
        }
    };
    console.log(params);
    //Write the DynamoDB table
    await dynamodb.put(params).promise();

    const sns_params = {
    Message: `Object is added`,
    Subject: 'Bucket Notification',
    TopicArn: process.env.SNS_TOPIC
}
// Send to SNS
const result = await sns.publish(sns_params).promise()
console.log(result)

} catch (error) {
  console.error(error);
}

};
