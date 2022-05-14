from pandas import json_normalize
import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url_username(username):
    # Replace with user ID below
    return "https://api.twitter.com/2/users/by/username/"+username


def create_url_getTweets(user_id):
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def create_url_getTweet(id):
    return "https://api.twitter.com/2/tweets/{}".format(id)


def create_url_search():
    return "https://api.twitter.com/2/tweets/search/recent"


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def get_params_search(param):
    # Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
    # expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
    query_param = {'query': param+' lang:es', 'max_results': 20}
    return query_param


def bearer_oauth(r):

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def getTweetsByUser(username):
    #GettingUserid
    url = create_url_username(username)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    userData = json.loads(json.dumps(json_response))

    #Getting User tweets
    url = create_url_getTweets(userData["data"]["id"])
    json_response = connect_to_endpoint(url, params)
    tweets = json.loads(json.dumps(json_response))['data']
    formatData = []
    i = 1
    for tweet in tweets:
      formatData.append([i, tweet['text']])
      i = i+1
    return formatData


def getTweet(id):
    url = create_url_getTweet(id)
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    tweetText = [[1, json.loads(json.dumps(json_response))['data']['text']]]
    return tweetText


def searchTweets(searchParam):
    url = create_url_search()
    params = get_params_search(searchParam)
    json_response = connect_to_endpoint(url, params)

    tweets = json.loads(json.dumps(json_response))['data']
    formatData = []
    i = 1
    for tweet in tweets:
      formatData.append([i, tweet['text']])
      i = i+1
    return formatData, json.dumps(json_response, indent=4, sort_keys=True)
