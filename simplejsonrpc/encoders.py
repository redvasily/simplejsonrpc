import datetime
import simplejson


class SafeEncoder(simplejson.JSONEncoder):
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

