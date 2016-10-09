# -*- coding: utf-8 -*-

import requests

class Ambient:
    def __init__(self, channelId, writeKey, *args):
        self.url = "http://ambidata.io/api/v2/channels/" + str(channelId) + "/data"
        self.writeKey = writeKey
        if len(args) >= 2:
            self.userKey = args[1]
        if len(args) >= 1:
            self.readKey = args[0]

    def send(self, data):
        data['writeKey'] = self.writeKey
        r = requests.post(self.url, json = data)
        return r
