from slackclient import SlackClient
import time # time for sleep between polls
import json # json for parse the rtm_read() data
import sys

# Slack API token
token = "xoxp-22279063781-22282485879-23302734596-cb3da71b11"

sc = SlackClient(token) # create an instance of a slack client

# send a test messgae
sc.api_call("api.test")
sc.api_call("channels.info", channel="1234567890")
sc.api_call(
    "chat.postMessage", channel="#general", text="Hello from Python! :tada:",
    username='gamebot', icon_emoji=':robot_face:'
)
sc.api_call(
    "chat.postMessage", channel="#general", text="Send a message and I'll read it!",
    username='gamebot', icon_emoji=':robot_face:'
)
# On connect - read from messaging feed every second
if sc.rtm_connect():
    while True:
        data = json.dumps(sc.rtm_read()) # turn data into JSON obj.
        print data
        sys.stdout.flush()
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
