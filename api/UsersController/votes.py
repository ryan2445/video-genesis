import boto3
import simplejson as json
import os

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def badRequest(msg):
    return {
        'statusCode': 400,
        'body': msg
    }

def votesGet(event, context):
    queryParams = event["queryStringParameters"]
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    required_keys = ['videoId']
    valid = all(key in queryParams for key in required_keys)
    if not valid: return badRequest('Missing required keys')

    vote = dynamodb.get_item(Key = { "pk": f"ID#{userId}", "sk": f"VOTE#{queryParams['videoId']}" }).get('Item')

    return {
        'statusCode': 200,
        'body': json.dumps({'vote': vote})
    }

def votesPost(event, context):
    #   Load request params
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    #   Validate request
    required_keys = ['videoId', 'videoUserId', 'upvoted']
    valid = all(key in body for key in required_keys)
    if not valid: return badRequest('Missing required keys')

    #   Get the user's vote for the video
    voteKey = { "pk": f"ID#{userId}", "sk": f"VOTE#{body['videoId']}" }
    vote = dynamodb.get_item(Key = voteKey).get('Item')
    #   If the vote in the request is null, delete the vote by making it the same as the current vote 
    if vote and body['upvoted'] == None: body['upvoted'] = vote['upvoted']

    #   Get the video they voted for and its likes / dislikes
    video = dynamodb.get_item(Key = { "pk": f"ID#{body['videoUserId']}", "sk": f"VIDEO#{body['videoId']}" })['Item']
    likes = video.get('likes') or 0
    dislikes = video.get('dislikes') or 0

    #   If user voted for the same thing they have already voted for - delete the vote
    if vote and (body['upvoted'] == vote['upvoted']):
        #   Delete the vote for the user
        dynamodb.delete_item(Key = voteKey)
        #   If the user likes a video they already liked - remove like
        if body['upvoted']: likes -= 1
        #   If the user disliked a video they alread disliked - remove dislike
        else: dislikes -= 1
    #   If user hasn't voted or voted for something they haven't voted for already - create/replace vote
    else:
        dynamodb.put_item(
            Item = {
                'pk': f"ID#{userId}",
                'sk': f"VOTE#{body['videoId']}",
                'videoId': body['videoId'],
                'userId': userId,
                'videoUserId': body['videoUserId'],
                'upvoted': bool(body['upvoted'])
            }
        )

        #   If user liked the video
        if body['upvoted']:
            #   User has already disliked the video - remove the dislike
            if vote: dislikes -= 1
            #   Add the like
            likes += 1
        #   If user disliked the video
        else:
            #   User has already liked the video - remove the like
            if vote: likes -= 1
            #   Add the dislike
            dislikes += 1
 
    dynamodb.update_item(
        Key = { "pk": video['pk'], "sk": video['sk'] },
        UpdateExpression = "set likes=:0,dislikes=:1",
        ExpressionAttributeValues = { ":0": likes, ":1": dislikes }
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'likes': likes, 'dislikes': dislikes})
    }

def handle(event, context):
    response = None
    
    methods = {
        'GET': votesGet,
        'POST': votesPost,
        'PUT': None,
        'DELETE': None
    }
    
    method = event['httpMethod']
    
    response = methods[method](event, context)

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