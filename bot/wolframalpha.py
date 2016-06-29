import xml.sax
import re
import urllib.request
import random

class WolframHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.data = ""
        self.rec = False
        
        self.interpretation = ""
        self.recInterpret = False

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "pod":
            if attributes["title"] == "Input interpretation":
                self.recInterpret = True
            if "primary" in attributes.keys() and attributes["primary"] == "true":
                self.rec = True
        if tag == "img":
            if self.rec:
                self.data = attributes["src"]
            elif self.recInterpret and "title" in attributes.keys():
                self.recInterpret = False
                self.interpretation = attributes["title"]

    def endElement(self, tag):
        if tag == "pod":
            self.rec = False
            self.recInterpret = False
        self.CurrentData = ""

    def characters(self, content):
        self.data

    def endDocument(self):
        self.interpretation = random.choice(["You want x? Here you go:", "x coming right up:", "x little cuck, just for you:"]).replace("x", re.sub("[\(\[].*?[\)\]]", "", self.interpretation).rstrip()))