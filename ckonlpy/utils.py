import glob
import os


installpath = os.path.dirname(os.path.realpath(__file__))

def load_dictionary(directory, encoding='utf-8', ignore_a_syllable=False):
    fnames = glob.glob('%s/*.txt' % directory)
    words = set()
    for fname in fnames:
        try:
            with open(fname, encoding=encoding) as f:
                words_ = {line.strip() for line in f}
                if ignore_a_syllable:
                    words_ = {w for w in words_ if len(w) > 1}
                words.update(words_)
        except Exception as e:
            print(e)
            continue
    return words

def loadtxt(fname, encoding='utf-8'):
    try:
        with open(fname, encoding=encoding) as f:
            return [line.strip() for line in f]
    except Exception as e:
        print(e)
        return []