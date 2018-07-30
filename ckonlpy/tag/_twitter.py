from ._abstract import AbstractTagger
from konlpy.tag import Twitter as KoNLPyTwitter
from ckonlpy.custom_tag import SimpleTemplateTagger
from ckonlpy.data.tagset import twitter as tagset
from ckonlpy.dictionary import CustomizedDictionary
from ckonlpy.utils import installpath
from ckonlpy.utils import load_dictionary


class Twitter(AbstractTagger):

    def __init__(self, dictionary=None, templates=None, use_twitter_dictionary=True):
        super().__init__(dictionary, templates)
        self._base = KoNLPyTwitter()
        self.use_twitter_dictionary = use_twitter_dictionary
        if use_twitter_dictionary:
            self._load_default_dictionary()
        self.tagset = tagset
        self.template_tagger = SimpleTemplateTagger(self.dictionary, templates)

    def _load_default_dictionary(self):
        directory = '%s/data/twitter/' % installpath
        self.dictionary.add_dictionary(
            load_dictionary('%s/josa' % directory), 'Josa')
        self.dictionary.add_dictionary(
            load_dictionary('%s/noun' % directory, ignore_a_syllable=True), 'Noun')
        self.dictionary.add_dictionary(
            load_dictionary('%s/adverb' % directory), 'Adverb')
        #self.dictionary.add_dictionary(
        #    load_dictionary(modifier_dir), 'Modifier')