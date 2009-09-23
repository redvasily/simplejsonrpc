from urllib import urlopen


class Error(Exception):
    pass

class JSONRPCException(Error):
    pass


class _Method(object):
    def __init__(self, send, name):
        self.__send = send
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__send, "%s.%s" % (self.__name, name))

    def __call__(self, *args):
        return self.__send(self.__name, args)


class ServiceProxy(object):
    def __init__(self, uri, encoder=None, decoder=None):
        self.__uri = uri

        if encoder is not None:
            self.__encoder = encoder
        else:
            from encoders import SafeEncoder
            self.__encoder = SafeEncoder()

        if decoder is not None:
            self.__decoder = decoder
        else:
            from decoders import SafeDecoder
            self.__decoder = SafeDecoder()


    def __request(self, methodname, params):
        data = self.__encoder.encode({
            'method': methodname,
            'params': params,
            'id':'jsonrpc'
        })
        respdata = urlopen(self.__uri, data).read()
        response = self.__decoder.decode(respdata)
        if response['error'] != None:
            raise JSONRPCException(response['error'])
        return response['result']

    def __repr__(self):
        return "<ServerProxy for %s>" % self.__uri

    __str__ = __repr__

    def __getattr__(self, name):
        # magic method dispatcher
        return _Method(self.__request, name)
