from json import JSONEncoder


class MyEncoder(JSONEncoder):
    def default(self, o):
        myDict = o.__dict__
        if 'lmc_match' in myDict:
            del myDict['lmc_match']
        return myDict
