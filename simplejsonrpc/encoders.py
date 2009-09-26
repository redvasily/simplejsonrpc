import new
import datetime
import simplejson


class SafeEncoder(simplejson.JSONEncoder):
    def __init__(self, *args, **kwds):
        utf8_output = kwds.pop('utf8_output', True)
        if utf8_output:
            kwds['ensure_ascii'] = False

        simplejson.JSONEncoder.__init__(self, *args, **kwds)

        if utf8_output:
            def encode(self, o):
                out = simplejson.JSONEncoder.encode(self, o)
                return out.encode('utf8')

            self.encode = new.instancemethod(encode, self, SafeEncoder)

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return {
                '__jsonclass__': ['datetime', o.year, o.month, o.day,
                    o.hour, o.minute, o.second, o.microsecond],
            }
        elif isinstance(o, datetime.date):
            return {
                '__jsonclass__': ['date', o.year, o.month, o.day],
            }
        else:
            super(SafeEncoder, self).default(o)
