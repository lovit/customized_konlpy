class CustomizedDictionary:
    def __init__(self):
        self._pos2words = {}
        
    def add_dictionary(self, words, tag):
        if type(words) == str:
            words = [words]
        wordset = self._pos2words.get(tag, set())
        wordset.update(set(words))
        self._pos2words[tag] = wordset
    
    def load_dictionary(self, fname_list, tag):
        def load(fname):
            try:
                with open(fname, encoding='utf-8') as f:
                    words = {word.strip() for word in f}
                    return words
            except Exception as e:
                print('load_dictionary error: %s'%e)
                return []
            
        wordset = self._pos2words.get(tag, set())
        for fname in fname_list:
            wordset.update(load(fname))
        self._pos2words[tag] = wordset

    def get_tags(self, word):
        return {tag for tag, words in self._pos2words.items() if word in words}
    
    def is_tag(self, word, tag):
        return word in self._pos2words.get(tag, {})