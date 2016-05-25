import logging
import random
import urllib
from __init__ import joke_list
logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "what are you, fucking gay?"
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['You are a dirty whore']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "uhh well.. erm- im a fucking idiot. fist me."
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        rand = random.randrange(len(joke_list))
        self.send_message(channel_id, joke_list[rand][0])
        if joke_list[rand][1]:
         self.clients.send_user_typing_pause(channel_id)
         self.send_message(channel_id, joke_list[rand][1])
         
    def write_error(self, channel_id, err_msg):
        txt = "a fucking error! what a surprise:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
        }
        self.clients.web.chat.post_message(channel_id, '', attachments=[attachment], as_user='true')

    def latex_equation(self, channel_id, msg_txt):
        if msg_txt.count('$') != 2:
            self.send_message(channel_id, "You're doing it wrong, little cuck.")
            return

        eqn = msg_txt.split('$', 2)[1]
        parsed = urllib.quote(eqn)
        #url = 'https://latex.codecogs.com/gif.latex?' + parsed
        url = 'http://chart.googleapis.com/chart?cht=tx&chl=' + parsed
    
        attachment = {
            "fallback": "Latex equation",
            "image_url": url,
        }
        self.clients.web.chat.post_message(channel_id, '', attachments=[attachment], as_user='true')
    
    def kys(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        kick = "/kys <@" + bot_uid + ">"
        self.send_message(channel_id, "goodbuy world, you have been a filthy whore.")
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, kick)
        self.clients.web.channels.kick(channel_id, bot_uid)
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, "fuck")
        
