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
        
        # Init a dict to map users
        userMap = {}

        def addUser(video):
            pk = video['pk']
            if pk in userMap:
                video["user"] = userMap[pk]
            else:
                # Get the user
                user = dynamodb.query(KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq('USER'), Limit=1)
                # If the user exists, attach them to the video
                if (user["Count"] >= 1):
                    video["user"] = user["Items"][0]
                    userMap[pk] = user["Items"][0]
            return video
        
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
                    video = resp['Items'][0]
                    
                    video = addUser(video)
                    
                    playlistItem["video"] = video
                    videoMap[videoSK] = video
            return playlistItem
        
        # Add the user to each video
        videos = [getVideo(v) for v in playlistItems]
        
        playlist['videos'] = videos
    else:
        playlist['videos'] = []
    
    # Query the user who made the playlist
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(playlistPK) & Key('sk').eq('USER'), Limit=1)
    
    # If we found the user, attach it to the response
    if response['Count'] >= 1:
        playlist['user'] = response['Items'][0]
    
    return playlist

def badRequest(msg: str) -> dict:
    return {
        'statusCode': 400,
        'body': msg
    }

def playlistsGet(event, context):
    queryParams = event['queryStringParameters']
    
    if queryParams and 'username' in queryParams:
        username = event['queryStringParameters']['username']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('playlist#'))
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

# Creates a new playlist
def playlistsPost(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']
    
    if 'playlistTitle' not in body:
        return badRequest('Error: playlistTitle required in request')

    #   Assemble playlist object
    pk = "ID#" + userId
    playlistSK = "playlist#" + str(uuid.uuid4())
    playlistTitle = body['playlistTitle']
    video = body.get('video', None)
    isPrivate = body.get('isPrivate', False)
    description = body.get('description', '')
    createdAt = datetime.datetime.now(timezone.utc).isoformat()
    
    if video is not None:
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
            'description': description,
            'createdAt': createdAt
        }
    )
    
    # Create the first playlist item
    if video is not None:
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

# Update a playlist with given data
def playlistsPut(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    pk = "ID#" + userId
    sk = body['sk']
    optional_keys = [
        'playlistTitle',
        'playlistThumbnail',
        'isPrivate',
        'description'
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

# Deletes some attributes based on a primary key and sort key
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
    
    if queryParams and 'username' in queryParams:
        username = event['queryStringParameters']['username']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('playlist#'))
    else:
        scan_kwargs = {
            'FilterExpression': Key('sk').begins_with('playlist') & Key('isPrivate').eq(False)
        }
        response = dynamodb.scan(**scan_kwargs) 
    
    videoSK = event['queryStringParameters']['videoSK']
    playlistWithVideo = []
    for playlist in response['Items']:
        resp = dynamodb.query(
            KeyConditionExpression = Key('pk').eq(playlist['sk']) & Key('sk').begins_with('playlist'),
            FilterExpression = Key('videoSK').eq(videoSK)
        )
        if resp['Count'] >= 1:
            playlistWithVideo.append(playlist['sk'])
            
    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': playlistWithVideo })
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
        resp = dynamodb.query(
            KeyConditionExpression = Key('pk').eq(playlist['sk']) & Key('sk').begins_with('playlistVideo#'),
            FilterExpression = Key('videoSK').eq(vid['sk']) & Key('videoPK').eq(vid['pk'])
        )
        
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
        
        resp = dynamodb.query(
            KeyConditionExpression = Key('pk').eq(playlist['sk']) & Key('sk').begins_with('playlistVideo#'),
            FilterExpression = Key('videoSK').eq(videoSK) & Key('videoPK').eq(videoPK)
        )
        
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

def getPlaylistsWithoutVideo(event, context):
    if 'userPK' not in event['queryStringParameters']:
        return badRequest("Error: userPK required in request")
    if 'videoSK' not in event['queryStringParameters']:
        return badRequest('Error: videoSK required in request')
    
    userPK = event['queryStringParameters']['userPK'] # ID{user}
    videoSK = event['queryStringParameters']['videoSK'] # playlist#{playlistID}
    
    # Query for user's playlists
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(userPK) & Key('sk').begins_with('playlist#'))
    
    # If the user has no playlists, return the empty array
    if response['Count'] <= 0:
        return {
            'statusCode': 200,
            'body': json.dumps([])
        }
    
    # Get the playlists
    playlists = response['Items'][0]
    
    # Clear the response
    response = []

    # Add each playlist to the response that does not have the video in question
    for playlist in playlists:
        playlistSK = playlist['sk']
        
        playlistItems = dynamodb.query(KeyConditionExpression = Key('pk').eq(playlistSK) & Key('sk').begins_with('playlistVideo#') & Key('videoSK').eq(videoSK))
        
        if playlistItems['Count'] == 0:
            response.append(playlist)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
def handle(event, context):
    response = None
    
    methods = {
        'GET': {
            '/playlists/all': playlistsGet,
            '/playlists': playlistGet,
            '/playlists/video': getPlaylistsByVideo,
            '/playlists/without-video': getPlaylistsWithoutVideo
        },
        'POST': {
            '/playlists': playlistsPost,
            '/playlists/add-videos': playlistAddVideos,
            '/playlists/delete-videos': playlistDeleteVideos,
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