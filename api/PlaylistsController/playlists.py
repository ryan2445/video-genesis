import boto3
from boto3.dynamodb.conditions import Key
import simplejson as json
import os
import uuid
import datetime
from datetime import timezone

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def getPlaylist_(playlistPK, playlistSK):
    # Get the playlist
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(playlistPK) & Key('sk').eq(playlistSK), Limit=1)
    
    # If the playlist does not exist, return an error
    if response['Count'] == 0:
        return None
    
    # Get the playlist
    playlist = response['Items'][0]
    
    # Get the videos attached to the playlist
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(playlistSK) & Key('sk').begins_with('playlistVideo#'))

    if response['Count'] > 0:
        playlistItems = response['Items']
        
        # Init a dict to map videos
        videoMap = {}

        def getVideo(playlistItem):
            videoPK = playlistItem['videoPK']
            videoSK = playlistItem['videoSK']
            
            if videoSK in videoMap:
                playlistItem["video"] = videoMap[videoSK]
            else:
                # Get the video
                resp = dynamodb.query(KeyConditionExpression = Key('pk').eq(videoPK) & Key('sk').eq(videoSK), Limit=1)
                
                # If the video exists, attach them to the playlistItem
                if (resp["Count"] >= 1):
                    print("got video for playlist")
                    video = resp['Items'][0]
                    playlistItem["video"] = video
                    videoMap[videoSK] = video
            return playlistItem
        
        # Add the user to each video
        videos = [getVideo(v) for v in playlistItems]
        
        playlist['videos'] = videos
    else:
        playlist['videos'] = []
    
    return playlist

def badRequest(msg: str) -> dict:
    return {
        'statusCode': 400,
        'body': msg
    }

#   Returns an array of all playlists for a given user
def playlistsGet(event, context):
    queryParams = event['queryStringParameters']
    
    if queryParams and 'username' in queryParams:
        username = event['queryStringParameters']['username']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('playlist'))
    else:
        scan_kwargs = {
            'FilterExpression': Key('sk').begins_with('playlist') & Key('isPrivate').eq(False)
        }
        response = dynamodb.scan(**scan_kwargs) 

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
    }

# Gets a playlist with all videos attached
def playlistGet(event, context):
    if 'pk' not in event['queryStringParameters']:
        return badRequest("Error: pk required in request")
    if 'sk' not in event['queryStringParameters']:
        return badRequest('Error: sk required in request')
    
    pk = event['queryStringParameters']['pk'] # ID{user}
    sk = event['queryStringParameters']['sk'] # playlist#{playlistID}
    
    playlist = getPlaylist_(pk, sk)
    
    if playlist is None:
        return badRequest('Error: Playlist does not exist')

    return {
        'statusCode': 200,
        'body': json.dumps(playlist)
    }

#   Creates a new playlist
def playlistsPost(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']
    
    if 'video' not in body:
        return badRequest("Error: video required in request")
    if 'playlistTitle' not in body:
        return badRequest('Error: playlistTitle required in request')

    #   Assemble playlist object
    pk = "ID#" + userId
    playlistSK = "playlist#" + str(uuid.uuid4())
    playlistTitle = body['playlistTitle']
    video = body['video']
    isPrivate = body.get('isPrivate', False)
    createdAt = datetime.datetime.now(timezone.utc).isoformat()
    
    # Ensure that the video exists
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(video['pk']) & Key('sk').eq(video['sk']), Limit=1)
    
    # If the video does not exist, return bad request
    if (response["Count"] == 0):
        badRequest("Error: Video does not exist")
    
    video = response['Items'][0]
    
    # Create the standard playlist entry
    response = dynamodb.put_item(
        Item = {
            'pk': pk,
            'sk': playlistSK,
            'playlistTitle': playlistTitle,
            'isPrivate': isPrivate,
            'createdAt': createdAt
        }
    )
    
    # Create the first playlist item
    response = dynamodb.put_item(
        Item = {
            'pk': playlistSK,
            'sk': 'playlistVideo#' + str(uuid.uuid4()),
            'videoPK': video['pk'],
            'videoSK': video['sk'],
            'createdAt': createdAt
        }
    )
    
    playlist = getPlaylist_(pk, playlistSK)

    return {
        'statusCode': 201,
        'body': json.dumps(playlist)
    }

#   Update a playlist with given data
def playlistsPut(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    pk = "ID#" + userId
    sk = body['sk']
    optional_keys = [
        'playlistTitle',
        'playlistThumbnail',
        'isPrivate'
    ]

    keys = list(filter(lambda x: body.get(x), optional_keys))
    if not keys: return badRequest("No attributes to update.")

    update_keys = []
    update_attributes = []
    for index, key in enumerate(keys):
        update_keys.append(f"{key}=:{index}")
        update_attributes.append((f":{index}", body.get(key)))
    
    response = dynamodb.update_item(
        Key = { 'pk': pk, 'sk': sk },
        UpdateExpression = f"set {', '.join(update_keys)}",
        ExpressionAttributeValues = dict(update_attributes)
    )

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': response })
    }

#   Deletes some attributes based on a primary key and sort key
def playlistsDelete(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    pk = "ID#" + userId
    sk = body['sk']

    response = dynamodb.delete_item(
        Key = {
            'pk': pk,
            'sk': sk
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': response })
    }
def getPlaylistsByVideo(event, context):
    queryParams = event['queryStringParameters']
    
    if queryParams and 'username' in queryParams and 'video' in queryParams:
        username = event['queryStringParameters']['username']
        video = event['queryStringParameters']['video']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('playlist') & Key('videos').contains(video))
    else:
        scan_kwargs = {
            'FilterExpression': Key('sk').begins_with('playlist') & Key('isPrivate').eq(False)
        }
        response = dynamodb.scan(**scan_kwargs) 

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
    }
    
def playlistAddVideos(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']
    
    if 'videos' not in body:
        return badRequest("Error: videos required in request")
    if 'sk' not in body:
        return badRequest('Error: sk required in request')
    
    
    pk = "ID#" + userId
    sk = body['sk']
    
    # Query for the playlist
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq(sk), Limit=1)

    # Ensure the playlist exists
    if response['Count'] <= 0:
        return badRequest('Error: Playlist does not exist')
    
    # Get the playlist
    playlist = response['Items'][0]
    
    # Get the videos to add
    videos = body['videos']
    
    # Get the createdAt time
    createdAt = datetime.datetime.now(timezone.utc).isoformat()
    
    # Add each video to the playlist
    for video in videos:
        videoPK = video['pk']
        videoSK = video['sk']
        
        # Query the video
        resp = dynamodb.query(KeyConditionExpression = Key('pk').eq(videoPK) & Key('sk').eq(videoSK), Limit=1)
        
        # Ensure the video exists
        if (resp['Count'] <= 0):
            continue
        
        # Get the video
        vid = resp['Items'][0]
        
        # Query the playlist item
        resp = dynamodb.query(KeyConditionExpression = Key('pk').eq(playlist['sk']) & Key('sk').begins_with('playlistVideo#') & Key('videoPK').eq(vid['pk']) & Key('videoSK').eq(vid['sk']), Limit=1)
        
        # If the playlist item already exists, continue
        if (resp['Count'] >= 1):
            continue
        
        # Create the playlist item
        response = dynamodb.put_item(
            Item = {
                'pk': playlist['sk'],
                'sk': 'playlistVideo#' + str(uuid.uuid4()),
                'videoPK': vid['pk'],
                'videoSK': vid['sk'],
                'createdAt': createdAt
            }
    )
        
    playlist = getPlaylist_(pk, sk)
    
    return {
        'statusCode': 200,
        'body': json.dumps(playlist)
    }
    
def playlistDeleteVideos(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']
    
    if 'videos' not in body:
        return badRequest("Error: videos required in request")
    if 'playlistTitle' not in body:
        return badRequest('Error: playlistTitle required in request')
    if 'sk' not in body:
        return badRequest('Error: sk required in request')
    
    
    pk = "ID#" + userId
    sk = body['sk']
    
    # Query for the playlist
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq(sk), Limit=1)

    # Ensure the playlist exists
    if response['Count'] <= 0:
        return badRequest('Error: Playlist does not exist')
    
    # Get the playlist
    playlist = response['Items'][0]
    
    # Get the videos to delete
    videos = body['videos']
    
    # For each video, delete it
    for video in videos:
        videoPK = video['pk']
        videoSK = video['sk']
        
        resp = dynamodb.query(KeyConditionExpression = Key('pk').eq(playlist['sk']) & Key('sk').begins_with('playlistVideo#') & Key('videoPK').eq(videoPK) & Key('videoSK').eq(videoSK), Limit=1)
        
        if resp['Count'] <= 0:
            print('could not find playlist item {videoPK} {videoSK}')
            continue
        
        playlistItem = resp['Items'][0]
        
        response = dynamodb.delete_item(
            Key = {
                'pk': playlistItem['pk'],
                'sk': playlistItem['sk']
            }
        )
    
    # query the fresh playlist
    playlist = getPlaylist_(pk, sk)
    
    return {
        'statusCode': 200,
        'body': json.dumps(playlist)
    }

def handle(event, context):
    response = None
    
    methods = {
        'GET': {
            '/playlists/all': playlistsGet,
            '/playlists': playlistGet,
            '/playlists/video': getPlaylistsByVideo 
        },
        'POST': {
            '/playlists': playlistsPost,
            '/playlists/add-videos': playlistAddVideos,
            '/playlist/delete-videos': playlistDeleteVideos,
        },
        'PUT': {
            '/playlists': playlistsPut
        },
        'DELETE': {
            '/playlists': playlistsDelete
        }
    }
    
    method = event['httpMethod']
    path = event['path']
    
    response = methods[method][path](event, context)

    if not response:
        response = {
            'statusCode': 404,
            'body': 'Not Found'
        }

    response['headers'] = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return response