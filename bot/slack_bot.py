import time
import logging
import traceback

from slack_clients import SlackClients
from messenger import Messenger
from event_handler import RtmEventHandler

logger = logging.getLogger(__name__)


def spawn_bot():
    return SlackBot()


class SlackBot(object):
    def __init__(self, token=None):
        """Creates Slacker Web and RTM clients with API Bot User token.

        Args:
            token (str): Slack API Bot User token (for development token set in env)
        """
        self.last_ping = 0
        self.keep_running = True
        if token is not None:
            self.clients = SlackClients(token)

    def _auto_ping(self):
        # hard code the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + 3:
            self.clients.rtm.server.ping()
            self.last_ping = now

    def stop(self, resource):
        """Stop any polling loops on clients, clean up any resources,
        close connections if possible.

        Args:
            resource (dict of Resource JSON): See message payloads - https://beepboophq.com/docs/article/resourcer-api
        """
        self.keep_running = False
