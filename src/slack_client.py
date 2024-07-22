import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackClient:
    def __init__(self, token, channel):
        self.client = WebClient(token=token)
        self.channel = channel

    def send_message(self, message):
        try:
            response = self.client.chat_postMessage(channel=self.channel, text=message)
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")