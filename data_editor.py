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

        words = text.split()
        # set each word to the normalized form
        for i in range(len(words)):
            # TODO removing the unnecessary words
            words[i] = Editor.MORPH.parse(words[i])[0].normal_form

        # TODO translation
        # detect the language of each word and translate into Russian
        # it will be done for convenience in further data mining

        return words