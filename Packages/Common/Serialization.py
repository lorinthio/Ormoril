import cPickle as pickle

def serialize(data):
    return pickle.dumps(data)

def deserialize(data):
    return pickle.loads(data)

def pack(message, data):
    return serialize({"message": message, "data": data})