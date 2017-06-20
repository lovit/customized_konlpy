from konlpy.tag import Twitter as KoNLPyTwitter
from customized_konlpy.dictionary import CustomizedDictionary

class Twitter:
    def __init__(self, customized_tagger=None):
        self._base = KoNLPyTwitter()
        self._customized_tagger = customized_tagger
        self._dictionary = CustomizedDictionary()
        self.tagset = self._base.tagset
        
    def pos(self, phrase):
        # TODO
        return self._base.pos(phrase)
    
    def nouns(self, phrase):
        tagged = self.pos(phrase)
        return [w for w, t in tagged if t[0] == 'N']
    
    def morphs(self, phrase, norm=False, stem=False):
        return [s for s, t in self.pos(phrase)]
    
    def phrases(self, phrase):
        # TODO
        return self._base.phrases(phrase)
    
    def add_dictionary(self, words, tag):
        if not (tag in self.tagset):
            raise ValueError('%s is not available tag' % tag)
        self._dictionary.add_dictionary(words, tag)
    
    def load_dictionary(self, fname_list, tag):
        if not (tag in self.tagset):
            raise ValueError('%s is not available tag' % tag)
        self._dictionary.load_dictionary(fname_list, tag)
    
    