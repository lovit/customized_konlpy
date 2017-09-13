# customized KoNLPy

한국어 자연어처리를 할 수 있는 파이썬 패키지, KoNLPy의 customized version입니다. 

customized_KoNLPy는 확실히 알고 있는 단어들에 대해서는 라이브러리를 거치지 않고 주어진 어절을 아는 단어들로 토크나이징 / 품사판별을 하는 기능을 제공합니다. 이를 위해 template 기반 토크나이징을 수행합니다.

    사전: {'아이오아이': 'Noun', '는': 'Josa'}
    탬플릿: Noun + Josa

위와 같은 단어 리스트와 탬플릿이 있다면 '아이오아이는' 이라는 어절은 [('아이오아이', 'Noun'), ('는', 'Josa')]로 분리됩니다.

## Todo list

1. 현재는 명사와 같이 스트링매치가 되는 단어에 대해서만 사용자 사전을 인식할 수 있습니다. 빠른 시간 내에 **동사/형용사에 대해서 활용이 되는 경우에도 인식**할 수 있는 기능을 넣을 예정입니다. 

1. 데이터 분석을 할 때 형태소 분석을 한 뒤 (1) 단어를 치환하거나, (2) 원하지 않는 단어들을 필터링 할 일들이 있습니다. 이를 위하여 **Postprocessing** 을 쉽게 할 수 있는 기능을 제공할 예정입니다. 

## Usage

### Part of speech tagging

KoNLPy와 동일하게 Twitter.pos(phrase)를 입력합니다. 각 어절별로 사용자 사전에 알려진 단어가 인식되면 customized_tagger로 어절을 분리하며, 사용자 사전에 알려지지 않은 단어로 구성된 어절은 트위터 형태소 분석기로 처리합니다. 

    twitter.pos('우리아이오아이는 이뻐요')

    > [('우리', 'Noun'), ('아이오', 'Noun'), ('아이', 'Noun'), ('는', 'Josa'), ('이뻐', 'Adjective'), ('요', 'Eomi')] 

'아이오아이'가 알려진 단어가 아니었기 때문에 트위터 분석기에서 단어를 제대로 인식하지 못합니다. 아래의 사용자 사전으로 단어 추가를 한 뒤 동일한 작업을 수행하면 아래와 같은 결과를 얻을 수 있습니다. 

    twitter.pos('우리아이오아이는 이뻐요')
    
    > [('우리', 'Modifier'), ('아이오아이', 'Noun'), ('는', 'Josa'), ('이뻐', 'Adjective'), ('요', 'Eomi')]


    twitter.pos('트와이스tt는 좋아요')

    > [('트와이스', 'Noun'), ('tt', 'Noun'), ('는', 'Josa'), ('좋', 'Adjective'), ('아요', 'Eomi')]

### Add words to dictioanry

ckonlpy.tag의 Twitter는 add_dictionary를 통하여 str 혹은 list of str 형식의 사용자 사전을 추가할 수 있습니다. 

    from ckonlpy.tag import Twitter

    twitter.add_dictionary('아이오아이', 'Noun')
    twitter.add_dictionary(['트와이스', 'tt'], 'Noun')

트위터 한국어 분석기에서 이용하지 않는 품사 (단어 클래스)를 추가하고 싶을 경우에는 반드시 force=True로 설정해야 합니다. 

    twitter.add_dictionary('lovit', 'Name', force=True)

### Add template to customized tagger

현재 사용중인 탬플릿 기반 토크나이저는 코드 사용 중 탬플릿을 추가할 수 있습니다. 현재 사용중인 탬플릿의 리스트는 아래처럼 확인할 수 있습니다. 

    twitter._customized_tagger.templates
    > [('Noun', 'Josa'), ('Modifier', 'Noun'), ('Modifier', 'Noun', 'Josa')]

탬플릿은 tuple of str 형식으로 입력합니다. 

    twitter._customized_tagger.add_a_template(('Noun', 'Noun', 'Josa'))

### Set templates tagger selector

Templates를 이용하여도 후보가 여러 개 나올 수 있습니다. 여러 개 후보 중에서 best 를 선택하는 함수를 직접 디자인 할 수 도 있습니다. 이처럼 몇 개의 점수 기준을 만들고, 각 기준의 weight를 부여하는 방식은 트위터 분석기에서 이용하는 방식인데, 직관적이고 튜닝 가능해서 매우 좋은 방식이라 생각합니다.

    score_weights = {
        'num_nouns': -0.1,
        'num_words': -0.2,
        'no_noun': -1
    }

    def my_score(candidate):
        num_nouns = len([w for w,t in candidate if t == 'Noun'])
        num_words = len(candidate)
        no_noun = 1 if num_nouns == 0 else 0

        score = (num_nouns * score_weights['num_nouns'] 
                 + num_words * score_weights['num_words']
                 + no_noun * score_weights['no_noun'])
        return score

위의 예제처럼 score_weights와 my_score 함수를 정의하여 twitter.set_selector()에 입력하면, 해당 함수 기준으로 best candidate를 선택합니다. 

    twitter.set_selector(score_weights, my_score)

## Install

    $ git clone https://github.com/lovit/customized_konlpy.git
    
    $ pip install customized_konlpy

## Requires

- JPype >= 0.6.1
- KoNLPy >= 0.4.4

