import boto3, os
from botocore.errorfactory import ClientError
import pandas as pd
from io import StringIO

def get_client():
    return boto3.client('s3')

def get_file(bucket, file_prefix, filename):
    # get s3 client
    s3_client = get_client()

    # read file data
    obj = s3_client.get_object(Bucket=bucket, Key= f'{file_prefix}/{filename}')
    body = obj['Body']

    # convert csv file data
    csv_string = body.read().decode('utf-8')

    # save csv data to dataframe
    df = pd.read_csv(StringIO(csv_string))

    return df