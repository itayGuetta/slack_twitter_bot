import argparse
import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime



def _get_command_line_args():
    parser = argparse.ArgumentParser()  # type: ArgumentParser
    parser.add_argument('--config_file', dest='path_to_json', help=" \n Please provid config file path for authentication  \n ",
                        required=True)
    parser.add_argument('--now', dest='flag_now', help=" \n Use this flag to run the bot now   \n",required=False)
    args = parser.parse_args()
    return args


def read_config_file(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def send_massage(client):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    try:
        response = client.chat_postMessage(channel='#content', text=current_time)
        assert response["message"]["text"] == current_time
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


def authenticate_slack(config_data):
    try:
        client = WebClient(token=config_data['SLACK']['SLACK_BOT_TOKEN'])
        return client
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


if __name__ == '__main__':
    args =_get_command_line_args()
    config_data = read_config_file(args.path_to_json)
    client = WebClient(token=config_data['SLACK']['SLACK_BOT_TOKEN'])
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


