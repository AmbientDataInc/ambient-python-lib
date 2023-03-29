class Ambient:
    def __init__(self, channelId, writeKey, readKey=None, userKey=None, ssl=False, debug=False):
        try:
            import urequests
            self.requests = urequests
            self.micro = True
        except ImportError:
            import requests
            self.requests = requests
            self.micro = False
        import time
        self.time = time

        self.channelId = channelId
        self.writeKey = writeKey
        self.readKey = readKey
        self.userKey = userKey
        self.ssl = ssl
        self.debug = debug

        if self.debug:
            self.url = 'http://192.168.33.13/api/v2/channels/' + str(channelId)
        else:
            if self.ssl and not self.micro:
                self.url = 'https://ambidata.io/api/v2/channels/' + str(channelId)
            else:
                self.url = 'http://ambidata.io/api/v2/channels/' + str(channelId)

        self.lastsend = 0

    def send(self, data, timeout = 30.0):
        millis = self.time.time() * 1000.0 if not self.micro else self.time.ticks_ms()
        if self.lastsend != 0 and (millis - self.lastsend ) < 4999:
            if self.micro:
                r = self.requests.Response(None)
            else:
                r = self.requests.Response()
            r.status_code = 403
            return r
        if isinstance(data, list):
            __d = data
        else:
            __d = [data]
        if self.micro:
            r = self.requests.post(self.url + '/dataarray', json = {'writeKey': self.writeKey, 'data': __d}, headers = {'Content-Type' : 'application/json'})
        else:
            r = self.requests.post(self.url + '/dataarray', json = {'writeKey': self.writeKey, 'data': __d}, headers = {}, timeout = timeout)
        millis = self.time.time() * 1000.0 if not self.micro else self.time.ticks_ms()
        self.lastsend = millis
        return r

    def read(self, **args):
        url = self.url + '/data'
        __o = []
        if hasattr(self, 'readKey'):
            __o.append('readKey=' + self.readKey)
        if 'date' in args:
            __o.append('date=' + args['date'])
        else:
            if 'start' in args and 'end' in args:
                __o.append('start=' + args['start'])
                __o.append('end=' + args['end'])
            else:
                if 'n' in args:
                    __o.append('n=' + str(args['n']))
                    if 'skip' in args:
                        __o.append('skip=' + str(args['skip']))
        if len(__o) > 0:
            url = url + '?' + '&'.join(__o)
        timeout = 30.0
        if 'timeout' in args:
            timeout = args['timeout']
        if self.micro:
            self.r = self.requests.get(url)
        else:
            self.r = self.requests.get(url, timeout = timeout)
        return list(reversed(self.r.json()))

    def getprop(self, **args):
        url = self.url
        if hasattr(self, 'readKey'):
            url = url + '?' + 'readKey=' + self.readKey
        timeout = 30.0
        if 'timeout' in args:
            timeout = args['timeout']
        if self.micro:
            self.r = self.requests.get(url)
        else:
            self.r = self.requests.get(url, timeout = timeout)
        self.prop = self.r.json()
        return self.prop

    def putcmnt(self, t, cmnt, timeout = 30.0):
        if self.micro:
            r = self.requests.put(self.url + '/data', json = {'writeKey': self.writeKey, 'created': t, 'cmnt': cmnt}, headers = {'Content-Type' : 'application/json'})
        else:
            r = self.requests.put(self.url + '/data', json = {'writeKey': self.writeKey, 'created': t, 'cmnt': cmnt}, headers = {}, timeout = timeout)
        return r

    def sethide(self, t, hide, timeout = 30.0):
        if self.micro:
            r = self.requests.put(self.url + '/data', json = {'writeKey': self.writeKey, 'created': t, 'hide': hide}, headers = {'Content-Type' : 'application/json'})
        else:
            r = self.requests.put(self.url + '/data', json = {'writeKey': self.writeKey, 'created': t, 'hide': hide}, headers = {}, timeout = timeout)
        return r
