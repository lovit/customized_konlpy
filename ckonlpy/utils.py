import os

installpath = os.path.dirname(os.path.realpath(__file__))

def loadtxt(fname, encoding='utf-8'):
    try:
        with open(fname, encoding=encoding) as f:
            docs = [line.strip() for line in f]
        return docs
    except Exception as e:
        print(e)
        return []