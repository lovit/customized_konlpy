from ckonlpy.utils import installpath

class SimpleTemplateTagger:

    def __init__(self, dictionary, templates=None, evaluator=None):

        if not evaluator:
            evaluator = SimpleEvaluator()

        self.dictionary = dictionary
        self.templates = _initialize_templates(templates, dictionary)
        self.evaluator = evaluator

    def pos(self, eojeol, debug=False):

        wordpos_nested_list = _match_words(
            eojeol, self.dictionary)

        template_matcheds = _match_templates(
            wordpos_nested_list, self.templates, debug)

        return template_matcheds

def _initialize_templates(templates, dictionary):
    if not templates:
        templatespath = '%s/data/templates/twitter_templates0' % installpath
        templates = loadtxt(templatespath)
        templates = [tuple(template.split()) for template in templates]

    single_words = [(pos, ) for pos in dictionary._pos2words]
    templates += [template for template in single_words
                  if not template in templates]

    return templates

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