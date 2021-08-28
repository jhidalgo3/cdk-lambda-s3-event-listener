from sys import path
import tarfile
import boto3
from io import BytesIO
from tarfile import TarInfo
import tempfile
import urllib
import os

s3_client = boto3.client('s3')
s3_resource=boto3.resource('s3')

def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    #key = event['Records'][0]['s3']['object']['key']
    key = urllib.parse.quote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))

    print('Bucket name: ', bucket)
    print('Object name: ', key)

    try:
        #input_tar_file = s3_client.get_object(Bucket=bucket, Key=key)
        #bytestream = BytesIO(input_tar_file['Body'].read())
        #with tarfile.open(fileobj = bytestream) as tar:
        #    # print(tar)
        #    for tar_resource in tar:
        #        # print(tar_resource.name)
        #        if tar_resource.isfile():
        #            inner_file_bytes = tar.extractfile(tar_resource).read()
        #            # print(inner_file_bytes)
        #            s3_client.upload_fileobj(BytesIO(inner_file_bytes), Bucket=bucket, Key=tar_resource.name)
        #    tar.close()

        # Decompress

        if not os.path.exists("/tmp/untar/"):
            os.mkdir("/tmp/untar/")

        filename = '/tmp/'+ key
        print('Target file: ' + filename)
        s3_client.download_file(bucket,key, filename)

        tar=tarfile.open(filename,mode="r:gz")
        for TarInfo in tar:
            print(TarInfo.name)
            if TarInfo.isfile():
                file_save=tar.extract(TarInfo.name,path="/tmp/untar/")
                s3_client.upload_file("/tmp/untar/"+TarInfo.name,bucket,TarInfo.name)
        tar.close()

        #with tempfile.NamedTemporaryFile(mode='wb') as temp:
        #    s3_client.download_file(bucket,key, temp)
        #    temp.seek(0)
        #    tar=tarfile.open(mode="r:gz",fileobj=temp )
        #    for TarInfo in tar:
        #        file_save=tar.extractfile(TarInfo.name,path="/tmp/untar/")
        #        s3_client.upload_fileobj(file_save,bucket,TarInfo.name)
        #    tar.close()
        #    temp.close()

        
        # Delete Tar.gz
        s3_client.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        raise e
