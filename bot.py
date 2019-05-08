import os
import time
import re
import requests
import json
import random
import datetime
import slack


BOT_ID = os.environ.get("SLACK_BOT_ID")
GIPHY_KEY = os.environ.get("GIPHY_API_KEY")


def get_random_gif(tag):
    """
    Fetch a random GIF from Giphy using tag
    """
    url = 'http://api.giphy.com/v1/gifs/random'
    params = {'api_key': GIPHY_KEY, 'tag': tag}
    resp = requests.get(url, params=params)
    data = resp.json()
    print(data)
    return data['data']['url']


def is_mention(id, command):
    """
    Return True if the user with ID id is mentioned in command
    """
    return id.lower() in command


@slack.RTMClient.run_on(event='message')
def handle_message(**payload):
    data = payload['data']
    command = data['text']
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']
    msg = ''

    webclient = payload['web_client']

    if "cake" in command:
        gif_url = get_random_gif("cookie cake")
        msg = "CAKE NOT AS GOOD AS COOKIE. MAYBE IT NUMBER 3 ALL-TIME DESSERT BEHIND COOKIE AND COOKIE CAKE\n" + gif_url
    elif is_mention(BOT_ID, command):
        msg = "WHO YOU CALLING MONSTER?!"
    elif "cookie" in command:
        gif_url = get_random_gif("cookie monster")
        msg = "DID SOMEONE SAY *COOKIE*?!\n" + gif_url
    
    if msg:
        webclient.chat_postMessage(
            channel=channel_id,
            text=msg,
            thread_ts=thread_ts
        )

if __name__ == "__main__":

    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()
