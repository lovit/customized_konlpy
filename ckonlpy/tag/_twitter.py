from konlpy.tag import Twitter as KoNLPyTwitter
from ckonlpy.custom_tag import SimpleTemplateTagger
from ckonlpy.custom_tag import SimpleSelector
from ckonlpy.data.tagset import twitter as tagset
from ckonlpy.dictionary import CustomizedDictionary
from ckonlpy.utils import installpath
from ckonlpy.utils import load_dictionary
from ckonlpy.utils import loadtxt


class Twitter:
    def __init__(self, use_twitter_dictionary=True):
        self._base = KoNLPyTwitter()
        self._dictionary = CustomizedDictionary()
        self._loaded_twitter_default_dictionary = use_twitter_dictionary
        if use_twitter_dictionary:
            self._load_default_dictionary()
        self._customized_tagger = self._load_customized_tagger()
        self.tagset = tagset
    
    def _load_customized_tagger(self):        
        templatespath = '%s/data/templates/twitter_templates0' % installpath
        templates = loadtxt(templatespath)
        templates = [tuple(template.split()) for template in templates]        
        return SimpleTemplateTagger(templates, self._dictionary, SimpleSelector())
    
    def _load_default_dictionary(self):
        directory = '%s/data/twitter/' % installpath
        self._dictionary.add_dictionary(load_dictionary('%s/josa' % directory), 'Josa')
        self._dictionary.add_dictionary(load_dictionary('%s/noun' % directory, ignore_a_syllable=True), 'Noun')
        self._dictionary.add_dictionary(load_dictionary('%s/adverb' % directory), 'Adverb')
        #self._dictionary.add_dictionary(load_dictionary(modifier_dir), 'Modifier')
        
    def pos(self, phrase):
        eojeols = phrase.split()
        tagged = []
        for eojeol in eojeols:
            tagged0 = self._customized_tagger.pos(eojeol)
            if tagged0:
                tagged += tagged0
                continue
            tagged += self._base.pos(eojeol)
        return tagged
    
    def nouns(self, phrase):
        tagged = self.pos(phrase)
        return [w for w, t in tagged if t == 'Noun']
    
    def morphs(self, phrase, norm=False, stem=False):
        return [s for s, t in self.pos(phrase)]
    
    def phrases(self, phrase):
        # TODO
        return self._base.phrases(phrase)
    
    def add_dictionary(self, words, tag, force=False):
        if (not force) and (not (tag in self.tagset)):
            raise ValueError('%s is not available tag' % tag)
        self._dictionary.add_dictionary(words, tag)
    
    def load_dictionary(self, fname_list, tag):
        if not (tag in self.tagset):
            raise ValueError('%s is not available tag' % tag)
        self._dictionary.load_dictionary(fname_list, tag)
    
    def set_selector(self, my_weight_dict, my_score_function):
        self._customized_tagger.set_selector(my_weight_dict, my_score_function)