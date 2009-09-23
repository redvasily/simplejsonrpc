import datetime
import simplejson


class SafeDecoder(simplejson.JSONDecoder):
    def __init__(self, *args, **kwds):
        kwds['object_hook'] = self.object_hook
        super(SafeDecoder, self).__init__(*args, **kwds)

    @staticmethod
    def object_hook(obj):
        if isinstance(obj, dict):
            try:
                jsonclass = obj['__jsonclass__']
                if jsonclass[0] == 'date':
                    return datetime.date(*jsonclass[1:])
                elif jsonclass[0] == 'datetime':
                    return datetime.datetime(*jsonclass[1:])
            except (KeyError, IndexError):
                pass

        return obj

