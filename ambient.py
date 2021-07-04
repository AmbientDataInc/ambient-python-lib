class Ambient:
    def __init__(self, channelId, writeKey, *args):
        try:
            import urequests
            self.requests = urequests
            self.micro = True
        except ImportError:
            import requests
            self.requests = requests
            self.micro = False

        self.channelId = channelId
        self.writeKey = writeKey
        self.debug = False
        if len(args) >= 3:
            self.debug = args[2]
        if len(args) >= 2:
            self.userKey = args[1]
        if len(args) >= 1:
            self.readKey = args[0]
        if self.debug:
            self.url = 'http://192.168.33.10/api/v2/channels/' + str(channelId)
        else:
            self.url = 'http://ambidata.io/api/v2/channels/' + str(channelId)

    def send(self, data, timeout = 30.0):
        if isinstance(data, list):
            __d = data
        else:
            __d = [data]
        if self.micro:
            r = self.requests.post(self.url + '/dataarray', json = {'writeKey': self.writeKey, 'data': __d}, headers = {'Content-Type' : 'application/json'})
        else:
            r = self.requests.post(self.url + '/dataarray', json = {'writeKey': self.writeKey, 'data': __d}, headers = {}, timeout = timeout)
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
