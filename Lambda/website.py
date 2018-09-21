import json
import os
import boto3
from botocore.exceptions import ClientError

def content_type(filename):
    filetype = "text/" + filename[filename.find(".")+1:]
    print('File type:' + filetype)
    return filetype

def lambda_handler(event, context):

    object = event['path']
    print(object)
    #strip initial / if, found
    loc = object.find("/")
    print(loc)
    if loc == 0:
        #remove initial / from object
        object = object[1:]

    print('attempting to get ' + object)
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(
            Bucket=os.environ['websitebucket'],
            Key=object
        )
        print('got file from s3')

        txt = response['Body'].read().decode('utf-8')

        return {
            "statusCode": 200,
            "headers": { "Content-Type": content_type(object) },
            "body": txt
        }
    except ClientError as ex:
        if ex.response['Error']['Code'] == 'NoSuchKey':
            print('404 error for '+ object)
            return { "statusCode": 404,
                        "body": "404"
            }
