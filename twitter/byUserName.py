import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAGI%2FZgEAAAAA0iVLwJq9lSR5p76p12Gm9H%2B2Y1g%3DVt4EGgLMXGXAZJ3bdjwb4DfcEKSSo0Nk0cb2l0AbUd068Zoce3'


def create_url_username():
    # Replace with user ID below
    username = 'HaciendaSV'
    return "https://api.twitter.com/2/users/by/username/"+username


def create_url_getTweets(user_id):
    # Replace with user ID below
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    #GettingUserid
    url = create_url_username()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    userData = json.loads(json.dumps(json_response))

    #Getting User tweets
    url = create_url_getTweets(userData["data"]["id"])
    json_response = connect_to_endpoint(url, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
