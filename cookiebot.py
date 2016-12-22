import os, time, re, requests, json
from slackclient import SlackClient

# constants
BOT_ID = os.environ.get("SLACK_BOT_ID")

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_command(command, channel):

    if "cookie" in command:
        gif_url = get_random_gif("cookie monster")
        try:
            slack_client.api_call("chat.postMessage", channel=channel, text="did someone say COOKIE?!\n" + gif_url, as_user=True)
        except Exception as e:
            print str(e)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    print output_list
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['user'] != BOT_ID:
                # return text
                return output['text'].lower(), output['channel']
    return None, None

def get_random_gif(tag):

    api_key = 'dc6zaTOxFJmzC'
    url = 'http://api.giphy.com/v1/gifs/random'

    params = { 'api_key': api_key, 'tag': tag}
    resp = requests.get(url, params=params)
    data = resp.json()

    return  data['data']['url']


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("CookieBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
