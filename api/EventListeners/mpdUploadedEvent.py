import re
import boto3
from boto3.dynamodb.conditions import Key
import json
from mpegdash.parser import MPEGDASHParser
import time

def handler(event, context):
    BucketKey = event['Records'][0]['s3']['object']['key']
    
    print('bucketKey', BucketKey)
    
    VideoKey = re.search('.+?(?=\/)', BucketKey).group(0)
    
    print('videoKey', VideoKey)

    db_client = boto3.resource('dynamodb').Table('system')
    
    while True:
        if not db_client.global_secondary_indexes or db_client.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
            print('Waiting for index to backfill...')
            time.sleep(5)
            db_client.reload()
        else:
            break
    
    resp = db_client.query(
        IndexName="videoKey-index",
        KeyConditionExpression=Key('videoKey').eq(VideoKey)
    )
    
    if len(resp['Items']) > 0:
        s3_client = boto3.client('s3')
        
        # Download the video metadata
        resp = s3_client.get_object(
            Bucket='genesis2vod-staging-output-q1h5l756',
            Key=BucketKey
        )
        
        # Decode the mpd data
        mpd_data = resp['Body'].read().decode('utf-8')
        
        # Parse the mpd file
        mpd = MPEGDASHParser.parse(mpd_data)
        
        # Parse the mpd data
        metadata = []
        representations = mpd.periods[0].adaptation_sets[0].representations
        for i in range(len(representations)):
            metadata.append({
                "id": representations[i].id,
                "width": representations[i].width,
                "height": representations[i].bandwidth,
                "codecs": representations[i].codecs,
                "scanType": representations[i].scan_type,
                "baseURL": representations[i].base_urls[0].base_url_value
            })
            
        metadata = json.dumps(metadata)
        
        # For each video, update the videoData
        for video in resp['Items']:
            print(video)
            pk = video['pk']
            sk = video['sk']
            
            response = db_client.update_item(
                Key={
                    'pk': pk,
                    'sk': sk
                },
                UpdateExpression="set videoData=:v",
                ExpressionAttributeValues={
                    ':v': metadata
                },
                ReturnValues="UPDATED_NEW"
            )
            
            print('response', response)
            
        
    return {
        'statusCode': 200,
        'body': json.dumps({'response': resp})
    }
