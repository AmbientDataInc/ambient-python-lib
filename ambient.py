# -*- coding: utf-8 -*-

import requests

class Ambient:
    def __init__(self, channelId, writeKey, *args):
        self.url = "http://ambidata.io/api/v2/channels/" + str(channelId) + "/dataarray"
        self.writeKey = writeKey
        if len(args) >= 2:
            self.userKey = args[1]
        if len(args) >= 1:
            self.readKey = args[0]

    def send(self, data):
        if isinstance(data, list):
            d = data
        else:
            d = [data]
        r = requests.post(self.url, json = {"writeKey": self.writeKey, "data": d})
        return r
