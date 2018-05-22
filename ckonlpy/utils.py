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

def load_wordset(fname, encoding='utf-8'):
    try:
        wordset = set()
        with open(fname, encoding=encoding) as f:
            for line in f:
                word = line.strip().split(' ')
                if len(word) == 1:
                    wordset.add(word[0])
                elif len(word) == 2:
                    wordset.add(tuple(word))
        return wordset
    except Exception as e:
        print(e)
        return set()

def load_replace_wordpair(fname, encoding='utf-8'):
    try:
        replace_wordset = {}
        with open(fname, encoding=encoding) as f:
            for line in f:
                try:
                    source, target = line.strip().split('\t')
                    source = source.split(' ')
                    if len(source) == 1:
                        source = source[0]
                    elif len(source) == 2:
                        source = tuple(source)
                    replace_wordset[source] = target
                except:
                    continue
        return replace_wordset
    except Exception as e:
        print(e)
        return {}