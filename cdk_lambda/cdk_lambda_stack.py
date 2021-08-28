# @author Jose Maria Hidalgo Garcia
# @email jhidalgo3@gmail.com
# @create date 2021-08-09 15:45:54
# @modify date 2021-08-09 15:45:54
# @desc AWS CDK Lambda + S3 Event Stack


from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
    core as cdk,
    aws_lambda_event_sources as event_src
)


class CdkLambdaStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create new IAM group and use
        #group = iam.Group(self, "jhidalgo3-VSGroup")
        #user = iam.User(self, "jhidalgo3-VSUser")
#
        ## Add IAM user to the group
        #user.add_to_group(group)

        # Create S3 Bucket
        bucket = s3.Bucket(self, 'jhidalgo3-vs-bucket',
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access= s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED
        )
        #.apply_removal_policy(cdk.RemovalPolicy.DESTROY)
        
        #bucket.grant_read_write(user)

        # Create a lambda function
        lambda_func = _lambda.Function(
            self, 'LambdaListener',
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler='LambdaListener.handler',
            code=_lambda.Code.asset('cdk_lambda/lambda'),
            environment={
                'BUCKET_NAME': bucket.bucket_name
            })

        bucket.grant_read_write(lambda_func)

        # Create trigger for Lambda function with image type suffixes
        notification = s3_notifications.LambdaDestination(lambda_func)
        notification.bind(self, bucket)
        bucket.add_object_created_notification(
            notification, s3.NotificationKeyFilter(suffix='.tar.gz'))

        #bucket.add_object_created_notification(
        #    notification, s3.NotificationKeyFilter(suffix='.jpg'))
        #bucket.add_object_created_notification(
        #    notification, s3.NotificationKeyFilter(suffix='.jpeg'))
        
        #lambda_func.add_event_source(
        #    event_src.S3EventSource(
        #        bucket, 
        #        events=[s3.EventType.OBJECT_CREATED],
        #        filters=[s3.NotificationKeyFilter(suffix='.jpg')]
        #    )
        #)
