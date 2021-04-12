import json
import boto3
import requests
import time

def lambda_handler(event, context):
    client = boto3.client('rekognition')
    s3_client = boto3.client('s3')
    # get basic info
    s3 = event['Records'][0]['s3']
    bucket = s3['bucket']['name']
    key = s3['object']['key']
    object_for_reko = {
        'S3Object':{
            'Bucket':bucket,
            'Name':key
        }
    }
    # print(object_for_reko)
    response = client.detect_labels(Image = object_for_reko)
    timestamp = time.time()
    labels = []
    # get all labels
    for i in range(len(response['Labels'])):
        labels.append(response['Labels'][i]['Name'])
    print(labels)
    # call headObject (for what?)
    # headObject_response = s3_client.head_object(
    #    Bucket = bucket,
    #    Key = key
    # )
    # sent to s3
    content = {
        'objectKey':key,
        'bucket':bucket,
        'createdTimestamp':timestamp,
        'labels':labels
    }
    host = "https://search-photos-msfvnxfd56ntszimne6hreskoq.ap-northeast-1.es.amazonaws.com"
    index = 'photos'
    type = 'photo'
    url = host + '/' + index + '/' + type
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data = json.dumps(content).encode("utf-8"), headers = headers)
    print(r)
    return {
        'statusCode': 200,
        'body': json.dumps('done! but no one can see this')
    }