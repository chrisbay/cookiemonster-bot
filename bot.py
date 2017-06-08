import os, time, re, requests, json, random, datetime
from slackclient import SlackClient

# constants
BOT_ID = os.environ.get("SLACK_BOT_ID")

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):
    
    # Write your own bot logic here!

    if is_mention(BOT_ID, command):
        post_to_slack(channel, "Who are you calling a monster?!")  
    elif "cookie" in command:
        gif_url = get_random_gif("cookie monster")
        post_to_slack(channel, "did someone say COOKIE?!\n", gif_url)


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
    
    print slack_rtm_output
    
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['user'] != BOT_ID:
                # return text
                return output['text'].lower(), output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
