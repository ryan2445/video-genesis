from mpegdash.parser import MPEGDASHParser
import boto3

client = boto3.client('s3')

response = client.get_object(
    Bucket='genesis2vod-staging-output-q1h5l756',
    Key='EvEABi1latkHGwtM-YiV0/EvEABi1latkHGwtM-YiV0.mpd'
)

mpd_data = response['Body'].read().decode('utf-8')

mpd = MPEGDASHParser.parse(mpd_data)

representations = mpd.periods[0].adaptation_sets[0].representations

metadata = []

for i in range(len(representations)):
    metadata.append({
        "id": representations[i].id,
        "width": representations[i].width,
        "height": representations[i].bandwidth,
        "codecs": representations[i].codecs,
        "scanType": representations[i].scan_type,
        "baseURL": representations[i].base_urls[0].base_url_value
    })
    
#print(metadata)    