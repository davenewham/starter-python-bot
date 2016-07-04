import logging
import random
import urllib
import math
import xml.sax
import re
import datetime

from math import *
from __init__ import joke_list

WHYREMID = ""
COMPUTINGID = "C18FPK5D4"
TILERID = "D1ARTBW49"

#from __init__ import sum_p
logger = logging.getLogger(__name__)
whySeed = 0


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
        greetings = [':hib: :solution: You are a whore']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)
        self.send_message(channel_id, user_id)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "uhh well.. erm - I'm a fucking idiot. Please don't hurt me. :samurai:"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        sum_p=0
        for i in range(1, len(joke_list)):
            sum_p=sum_p+joke_list[i][0]
        count_p=0
        joke_index=0
        rand = random.randrange(0, sum_p)
        for joke in joke_list:
            count_p=count_p+joke[0] 
            if count_p > rand:
                break
            joke_index=joke_index+1
        sum_p=0 
        for i in range(1, len(joke_list)):
            if i != joke_index:
                joke_list[i][0]=floor(joke_list[i][0]*(1.135))
                if joke_list[i][0]>256:
                    joke_list[i][0]=256
        joke_list[joke_index][0]= floor(joke_list[joke_index][0]-2*sqrt(joke_list[joke_index][0]))
        self.send_message(channel_id, joke_list[joke_index][1])
        if len(joke_list[joke_index]) > 2:
         self.clients.send_user_typing_pause(channel_id)
         self.send_message(channel_id, joke_list[joke_index][2])
         
    def write_error(self, channel_id, err_msg):
        txt = "a fucking :hib: error! what a surprise:\n>```{}```".format(err_msg)
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
            self.send_message(channel_id, "You're doing it wrong, little cuck. :hib:")
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
        self.send_message(channel_id, ":solution: goodbuy world, you have been a filthy whore. :solution:")
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, kick)
        self.clients.web.channels.kick(channel_id, bot_uid)
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, "fuck")
        #self.send_message(channel_id, channel_id)

    def startWhy(self, seed, chid, usid):
        rand = ""
        #self.send_message(chid, "/remind <@" + usid + "> g in 5 seconds")
        #self.clients.web.reminders.add("cuck!", 10, usid)

    def askWhy(self, channel_id, whyLength):
        rand = rand
        fp = open('./resources/why.txt', 'r')
        #for (

    def wolframalpha(self, query, channel_id):
        #Do not overuse this - Limited to 2000 requests/per month
        #what if we shuffled through several api keys? 
        apikey = ""

        query = query.replace("<@U1ARZ5PQS>:", "")
        query = query.replace("<@U1ARZ5PQS>", "")
        query = query.lstrip()
        query = urllib.quote_plus(query)

        url = "http://api.wolframalpha.com/v2/query?input=" + query + "&appid=" + apikey
        httpsocket = urllib.urlopen(url)
        httpbody = httpsocket.read()
        httpsocket.close()

        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        Handler = WolframHandler()
        xml.sax.parseString(httpbody, Handler)

        if Handler.interpretation != "":
            self.send_message(channel_id, Handler.interpretation)

        for key, value in Handler.data.iteritems():
            self.send_message(channel_id, key)
            attachment = {
                "fallback": key,
                "image_url": value,
            }
            self.clients.web.chat.post_message(channel_id, '', attachments=[attachment], as_user='true')

        if not Handler.data:
            self.send_message(channel_id, random.choice(["I haven't got a fucking clue","Why do you expect me to know cuck?","Can't be arsed","I don't know, I will ask ur mum"]))

class WolframHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.data = {}
        self.rec = False
        
        self.interpretation = ""
        self.recInterpret = False

    def startElement(self, tag, attributes):
        if tag == "pod":
            self.CurrentData = attributes["title"]
            if attributes["title"] == "Input interpretation":
                self.recInterpret = True
            self.rec = True
        if tag == "img":
            if self.recInterpret and "title" in attributes.keys():
                self.recInterpret = False
                self.interpretation = attributes["title"]
            elif self.rec:
                self.data[self.CurrentData] = attributes["src"]

    def endElement(self, tag):
        if tag == "pod":
            self.rec = False
            self.recInterpret = False
        self.CurrentData = ""

    def endDocument(self):
        if self.interpretation != "":
            bracketStrip = re.sub("[\(\[].*?[\)\]]", "", self.interpretation)
            whiteSpaceStrip = bracketStrip.rstrip()
            choice = random.choice(["You want the x? Here you go cuck!", "x coming right up cuck:", "x little cuck, just for you:"])
            self.interpretation = choice.replace("x", whiteSpaceStrip)
