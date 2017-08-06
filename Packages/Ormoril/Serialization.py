import cPickle as pickle

def serialize(data):
    return pickle.dumps(data)

def deserialize(data):
    try:
        return pickle.loads(data)
    except EOFError as error:
        return None
    except Exception:
        return None

def pack(message, data):
    return serialize({"message": message, "data": data})