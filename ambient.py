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

        self.url = 'http://ambidata.io/api/v2/channels/' + str(channelId) + '/dataarray'
        self.channelId = channelId
        self.writeKey = writeKey
        if len(args) >= 2:
            self.userKey = args[1]
        if len(args) >= 1:
            self.readKey = args[0]

    def send(self, data, timeout = 5.0):
        if isinstance(data, list):
            __d = data
        else:
            __d = [data]
        headers = {'Content-Type' : 'application/json'} if self.micro else {}
        r = self.requests.post(self.url, json = {'writeKey': self.writeKey, 'data': __d}, headers = headers, timeout = timeout)
        return r

    def read(self, **args):
        url = 'http://ambidata.io/api/v2/channels/' + str(self.channelId) + '/data'
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
        self.r = self.requests.get(url)
        return list(reversed(self.r.json()))

    def getprop(self):
        url = 'http://ambidata.io/api/v2/channels/' + str(self.channelId)
        if hasattr(self, 'readKey'):
            url = url + '?' + 'readKey=' + self.readKey
        self.r = self.requests.get(url)
        self.prop = self.r.json()
        return self.prop
