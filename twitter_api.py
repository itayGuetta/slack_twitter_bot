import requests
import os
import json
from datetime import datetime
# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def read_config_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data

def auth(file_path):
    data = read_config_file(file_path)
    return data['Twitter']['BEARER_TOKEN']


def create_url_find_user():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=PythonWeekly,realpython,fullstackpython"
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url

def create_url_tweete_from_user(user_id):
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


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_tweetes_by_user(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()



def get_ids_of_usernames(json_data):
    ids = []
    print(json_data)
    for user in json_data['data']:
        print(user)
        ids.append(user['id'])
    return ids

def calculate_one_hour(now,created):

    NUMBER_OF_SECONDS = 86400  # seconds in 24 hours
    first = datetime(2017, 10, 10)
    second = datetime(2017, 10, 12)
    if (first - second).total_seconds() > NUMBER_OF_SECONDS:
        print("its been over a day!")




def main():
    bearer_token = auth("/qmaster_bot_slack_twitter/config.json")
    url = create_url_tweete_from_user("373620985")
    headers = create_headers(bearer_token)
    params = get_params()
    json_response = get_tweetes_by_user(url, headers,params)
    # print(get_ids_of_usernames(json_response))
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()