# @author Jose Maria Hidalgo Garcia
# @email jhidalgo3@gmail.com
# @create date 2021-08-09 15:45:54
# @modify date 2021-08-09 15:45:54
# @desc AWS CDK Lambda + S3 Event Stack


import boto3
import os

s3 = boto3.client('s3')


def handler(event, context):
    bucket_name = (os.environ['BUCKET_NAME'])
    key = event['Records'][0]['s3']['object']['key']

    try:
        # Log the event
        print("[LambdaListenet] New file with name {} created in bucket {}".format(
            key, bucket_name))

        response = {'status': 'success', 'key': key}
        return response

    except Exception as e:
        print(e)
        print("[Error] :: Error processing file {} from bucket {}. ".format(
            key, bucket_name))
        raise e
