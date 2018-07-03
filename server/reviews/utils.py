import json

class JsonConvert(object):
    mappings = {}

    @classmethod
    def complex_handler(cls, Obj):
        if hasattr(Obj, '__dict__'):
            return Obj.__dict__
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))

    @classmethod
    def to_json(cls, obj):
        return json.dumps(obj.__dict__, default=cls.complex_handler)

    @classmethod
    def from_json(cls, json_str):
        return json.loads(json_str)
