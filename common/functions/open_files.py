import json


def get_json(filename) :
    """
    Given a json filename, return the corresponding python object.
    """
    result =  json.load(open(filename,'r'))
    return  result
