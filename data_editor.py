# this module is used for clearing the data from the unimportant information
# and for splitting the sentences into words
import pymorphy2
from yandex_translate import *
import re


class Editor:
    MORPH = pymorphy2.MorphAnalyzer()
    TRANSLATOR = YandexTranslate('trnsl.1.1.20160811T105153Z.8415630e3a8a61d6.'
                                 '9c2541d04cafd7784e06d6165152eb47355bdac9')

    # regular expressions
    HASHTAG_RE = re.compile('#[^\W_ ]+', re.U | re.I)
    RESPONSE_RE = re.compile('\[(id)\d*\|[^\W\d_ ]+\]', re.U)
    UNNECESSARY_RE = re.compile('[^\p\w\U0001F600-\U0001F637\U00002764]+|[\d]', re.U)

    # human smiles + heart smile
    SMILES_RE = re.compile('[\U0001F600-\U0001F637\U00002764]', re.U)

    @staticmethod
    def checkFakeWord(expr):
        word = expr.group(0)[1:]
        # if the word is a fake and isn't so widened, we delete this word from the sentence
        if str(Editor.MORPH.parse(word)[0]\
                       .methods_stack[0][0]) == '<FakeDictionary>':
            return ''
        # otherwise we return the word as it is, but without a hashtag
        return word

    @staticmethod
    def separateSmile(expr):
        smile = expr.group(0)
        return ' ' + smile + ' '

    @staticmethod
    def clean(text):
        # all the world in lowercase
        text = text.lower()

        # clear all hash tags and turn them to the simple words
        text = Editor.HASHTAG_RE.sub(Editor.checkFakeWord, text)

        # remove all response words such as [id111111111|анна]
        text = Editor.RESPONSE_RE.sub('', text)

        # remove all characters except whitespace, letters and smiles
        text = Editor.UNNECESSARY_RE.sub(' ', text)

        # separate the smiles into the words
        text = Editor.SMILES_RE.sub(Editor.separateSmile, text)

        # detect the language of each word and translate into Russian
        # it will be done for convenience in further data mining
        try:
            lang = Editor.TRANSLATOR.detect(text)

            if lang != 'ru':
                text = Editor.TRANSLATOR.translate(text, lang = 'ru')['text']

            words = text.split()
        except (YandexTranslateException, AttributeError):
            # if there is something wrong with detecting the languate
            # and/or translation, return nothing
            return None
        else:
            # set each word to the normalized form
            i = 0
            while i < len(words):
                # removing the unnecessary words
                wordProperty = Editor.MORPH.parse(words[i])[0]
                # more about analysis in the documentation:
                # http://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
                if wordProperty.normalized.tag.POS in {'NUMR','NPRO','PREP', 'CONJ'}:
                    words.remove(words[i])
                    i -= 1
                else:
                    # normalization
                    words[i] = wordProperty.normal_form

                i += 1
            print(words)
            return words