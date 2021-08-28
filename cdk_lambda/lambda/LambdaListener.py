from sys import path
import tarfile
import boto3
from io import BytesIO
from tarfile import TarInfo
import tempfile
import urllib
import os
import mimetypes

s3_client = boto3.client('s3')
s3_resource=boto3.resource('s3')

def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.quote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))

    print('Bucket name: ', bucket)
    print('Object name: ', key)

    try:
        if not os.path.exists("/tmp/untar/"):
            os.mkdir("/tmp/untar/")

        filename = '/tmp/'+ key
        print('Target file: ' + filename)
        s3_client.download_file(bucket,key, filename)

        tar=tarfile.open(filename,mode="r:gz")
        for TarInfo in tar:
            if TarInfo.isfile():
                file_save=tar.extract(TarInfo.name,path="/tmp/untar/")
                file_mime_type, _ = mimetypes.guess_type("/tmp/untar/"+TarInfo.name)
                print (file_mime_type)
                if file_mime_type is None:
                    file_mime_type = "application/json"
                s3_client.upload_file("/tmp/untar/"+TarInfo.name,bucket,TarInfo.name,ExtraArgs={'ContentType': file_mime_type})
        tar.close()
        
        # Delete Tar.gz
        s3_client.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        raise e
