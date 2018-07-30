from ckonlpy.custom_tag import SimpleTemplateTagger
from ckonlpy.dictionary import CustomizedDictionary

class AbstractTagger:

    def __init__(self, dictionary=None, templates=None):
        self.dictionary = dictionary if dictionary else CustomizedDictionary()
        self.template_tagger = SimpleTemplateTagger(self.dictionary, templates)

    def pos(self, phrase, norm=False, stem=False, perfect_match=False):

        def has_None(wordpos_list):
            return len([True for _, pos, _, _ in wordpos_list if pos is None]) > 0

        eojeols = phrase.split()
        tagged = []

        for eojeol in eojeols:

            wordpos_list = self.template_tagger.pos(eojeol, perfect_match)

            if not wordpos_list:
                tagged += self._base.pos(eojeol, norm=norm, stem=stem)
                continue

            for word, pos, _, _ in wordpos_list:
                if pos is not None:
                    tagged.append((word, pos))
                    continue
                for word_, pos_ in self._base.pos(word, norm=norm, stem=stem):
                    tagged.append((word_, pos_))
        return tagged

    def nouns(self, phrase):
        tagged = self.pos(phrase)
        return [w for w, t in tagged if t == 'Noun']

    def morphs(self, phrase, norm=False, stem=False):
        return [s for s, t in self.pos(phrase, norm=norm, stem=stem)]

    def phrases(self, phrase):
        # TODO
        return self._base.phrases(phrase)

    def add_dictionary(self, words, tag, force=False):
        if (not force) and (not (tag in self.tagset)):
            raise ValueError('%s is not available tag' % tag)
        self.dictionary.add_dictionary(words, tag)

    def load_dictionary(self, fname_list, tag):
        if not (tag in self.tagset):
            raise ValueError('%s is not available tag' % tag)
        self.dictionary.load_dictionary(fname_list, tag)

    def add_a_template(self, a_template):
        self.template_tagger.add_a_template(a_template)

    def set_evaluator(self, my_weight_tuple, my_evaluate_function, test=True):
        self.template_tagger.set_evaluator(my_weight_tuple, my_evaluate_function, test)