import json
import logging
import re
import datetime

logger = logging.getLogger(__name__)

COMPUTINGID = "C18FPK5D4"
TILERID = "D1ARTBW49"

class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

        self.msg_writer.startWhy(TILERID);

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def _handle_message(self, event):
        # Filter out messages from the bot itself
        if 'user' not in event.keys():
            return
        if True:#not self.clients.is_message_from_me(event['user']):
            
            
            msg_txt = event['text']
            
            if self.clients.is_bot_mention(msg_txt):
                # e.g. user typed: "@pybot tell me a joke!"
                if 'help' in msg_txt:
                    self.msg_writer.write_help_message(event['channel'])
                elif 'latex' in msg_txt:
                    self.msg_writer.latex_equation(event['channel'], msg_txt)
                elif re.search('hi|hey|hello|howdy|cuck|gay', msg_txt):
                    self.msg_writer.write_greeting(event['channel'], event['user'])
                elif 'joke' in msg_txt:
                   self.msg_writer.write_joke(event['channel'])
                elif 'attachment' in msg_txt:
                    self.msg_writer.demo_attachment(event['channel'])
                elif 'kill yourself' in msg_txt:
                    self.msg_writer.kys(event['channel'])
                elif '?' in msg_txt:
                    self.msg_writer.wolframalpha(msg_txt, event['channel'])
                else:
                    self.msg_writer.write_prompt(event['channel'])
