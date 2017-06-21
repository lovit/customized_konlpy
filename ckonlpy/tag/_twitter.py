from konlpy.tag import Twitter as KoNLPyTwitter
from ckonlpy.custom_tag import SimpleTemplateTagger
from ckonlpy.data.tagset import twitter as tagset
from ckonlpy.dictionary import CustomizedDictionary
from ckonlpy.utils import installpath
from ckonlpy.utils import loadtxt


class Twitter:
    def __init__(self, load_default_dictionary=False):
        self._base = KoNLPyTwitter()
        self._dictionary = CustomizedDictionary()
        if load_default_dictionary:
            self._load_default_dictionary()
        self._customized_tagger = self._load_customized_tagger()
        self.tagset = tagset
    
    def _load_customized_tagger(self):        
        templatespath = '%s/data/templates/twitter_templates0' % installpath
        templates = loadtxt(templatespath)
        templates = [tuple(template.split()) for template in templates]
        selector = TwitterSelector()
        return SimpleTemplateTagger(templates, self._dictionary, selector)
    
    def _load_default_dictionary(self):
        josapath = '%s/data/twitter/josa.txt' % installpath
        modifierpath = '%s/data/twitter/modifier.txt' % installpath
        self._dictionary.add_dictionary(loadtxt(josapath), 'Josa')
        self._dictionary.add_dictionary(loadtxt(modifierpath), 'Modifier')
        
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
        return [w for w, t in tagged if t[0] == 'N']
    
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


class TwitterSelector:
    def __init__(self):
        self.weight = {
            'noun_length': 1,
            'noun_numbers': -0.2,
            'wordlist_length': -0.1,
            'no_noun': -0.5
        }

    def select(self, candidates):
        scores = []
        for candidate in candidates:
            noun_length = sum([len(w) for w, t in candidate if t == 'Noun'])
            noun_numbers = len([1 for w, t in candidate if t == 'Noun'])
            wordlist_length = len(candidate)
            no_noun = 0 if [1 for w, t in candidate if t == 'Noun'] else 1
            score = noun_length * self.weight.get('noun_length', 0) + noun_numbers * self.weight.get('noun_numbers', 0) + wordlist_length * self.weight.get('wordlist_length', 0) + no_noun * self.weight.get('no_noun', 0)
            scores.append(score)
        best = sorted(enumerate(scores), key=lambda x:x[1], reverse=True)[0][0]
        return candidates[best]