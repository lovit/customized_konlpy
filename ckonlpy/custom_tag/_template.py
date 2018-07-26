class SimpleTemplateTagger:
    def __init__(self, templates, dictionary, selector=None):
        self.templates = templates
        self.dictionary = dictionary
        # self.selector = selector if selector else SimpleSelector()

    def pos(self, eojeol, debug=False):

        wordpos_nested_list = _match_words(
            eojeol, self.dictionary)

        template_matcheds = _match_templates(
            wordpos_nested_list, self.templates, debug)

        return template_matcheds

def _match_words(eojeol, dictionary):
    n = len(eojeol)

    matched = []
    for b in range(n):
        sublist = []
        for e in range(b+1, min(n, b + dictionary._max_length) + 1):
            word = eojeol[b:e]
            for tag in dictionary.get_tags(word):
                sublist.append((word, tag, b, e))
        matched.append(sublist)
    return matched

def _match_templates(wordpos_nested_list, templates, debug=False):

    n = len(wordpos_nested_list)
    matcheds = []

    # for each begin position
    for wordpos_list in wordpos_nested_list:
        # for each (word, pos, begin, end)
        for wordpos in wordpos_list:
            # for each template
            for template in templates:
                if template[0] == wordpos[1]:
                    expandeds = _expand(
                        wordpos, template, wordpos_nested_list, n, debug)
                    matcheds += expandeds

    return matcheds

def _expand(wordpos, template, wordpos_nested_list, n, debug):

    def get_matched_wordpos(wordpos_list, tag):
        return [wordpos for wordpos in wordpos_list if wordpos[1] == tag]

    # Initialize candidates
    candidates = [[wordpos]]

    # Expansion
    for match_tag in template[1:]:
        candidates_ = []
        for candidate in candidates:
            last_index = candidate[-1][3]
            if last_index >= n:
                continue
            expandables = get_matched_wordpos(
                wordpos_nested_list[last_index], match_tag)
            for expandable in expandables:
                expanded = [c for c in candidate] + [expandable]
                candidates_.append(expanded)
        candidates = candidates_

    if debug and candidates:
        print('\ntemplate = {}'.format(template))
        for candidate in candidates:
            print(candidate)

    return candidates

class SimpleSelector:
    def __init__(self):
        self.weight = {
            'max_length_of_noun': 0.5,
            'num_of_nouns': -0.2,
            'num_of_words': -0.1,
            'num_noun_is_zero': -0.5
        }

    def select(self, candidates):
        scores = []
        for candidate in candidates:
            score = self.score(candidate)
            scores.append(score)
        best = sorted(enumerate(scores), key=lambda x:x[1], reverse=True)[0][0]
        return candidates[best]

    def score(self, candidate):
        num_of_nouns = len([1 for w, t in candidate if t == 'Noun'])
        if num_of_nouns:
            max_length_of_noun = max([len(w) for w, t in candidate if t == 'Noun'])
        else:
            max_length_of_noun = 0
        num_of_words = len(candidate)
        num_noun_is_zero = 0 if num_of_nouns else 1

        return (max_length_of_noun * self.weight.get('max_length_of_noun', 0)
                + num_of_nouns * self.weight.get('noun_numbers', 0)
                + num_of_words * self.weight.get('num_of_words', 0)
                + num_noun_is_zero * self.weight.get('num_noun_is_zero', 0)
               )