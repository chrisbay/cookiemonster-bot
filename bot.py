import os
import time
import re
import requests
import json
import random
import datetime
from slackclient import SlackClient


BOT_ID = os.environ.get("SLACK_BOT_ID")
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel, user):
    if "cake" in command:
        gif_url = get_random_gif("cookie cake")
        post_to_slack(channel, "CAKE NOT AS GOOD AS COOKIE. MAYBE IT NUMBER 3 ALL-TIME DESSERT BEHIND COOKIE AND COOKIE CAKE\n", gif_url)
    elif is_mention(BOT_ID, command):
        post_to_slack(channel, "WHO YOU CALLING MONSTER?!")  
    elif "cookie" in command:
        gif_url = get_random_gif("cookie monster")
        post_to_slack(channel, "DID SOMEONE SAY *COOKIE*?!\n", gif_url)


def get_random_gif(tag):
    """ 
    Fetch a random GIF from Giphy using tag
    """
    api_key = 'dc6zaTOxFJmzC'
    url = 'http://api.giphy.com/v1/gifs/random'
    params = { 'api_key': api_key, 'tag': tag}
    resp = requests.get(url, params=params)
    data = resp.json()
    return  data['data']['url']
    

def is_mention(id, command):
    """
    Return True if the user with ID id is mentioned in command
    """
    return id.lower() in command 


def post_to_slack(channel, msg, url=''):
    """
    Post msg to channel, optionally with a url
    """
    slack_client.api_call("chat.postMessage", channel=channel, text=(msg + url), as_user=True)


def parse_slack_output(slack_rtm_output):
    print(slack_rtm_output)
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['user'] != BOT_ID:
                # return text
                return output['text'].lower(), output['channel'], output['user']
    return None, None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Bot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
