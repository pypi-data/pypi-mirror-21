# -*- utf-8 -*-
from __future__ import print_function, unicode_literals, division, absolute_import

import os.path

import pkg_resources

from . import cedict
from . import rules
from epitran.ligaturize import ligaturize


class MissingData(Exception):
    pass


class Epihan(object):
    punc = [(u'\uff0c', u','),
            (u'\uff01', u'!'),
            (u'\uff1f', u'?'),
            (u'\uff1b', u';'),
            (u'\uff1a', u':'),
            (u'\uff08', u'('),
            (u'\uff09', u')'),
            (u'\uff3b', u'['),
            (u'\uff3d', u']'),
            (u'\u3010', u'['),
            (u'\u3011', u']'),
            ]

    def __init__(self, ligatures=False, cedict_file=None, rules_file='pinyin-to-ipa.txt'):
        if not cedict_file:
            raise MissingData('Please specify a location for the CC-CEDict file.')
        rules_file = os.path.join('data', 'rules', rules_file)
        rules_file = pkg_resources.resource_filename(__name__, rules_file)
        self.cedict = cedict.CEDictTrie(cedict_file)
        self.rules = rules.Rules([rules_file])

    def normalize_punc(self, text):
        for a, b in self.punc:
            text = text.replace(a, b)
        return text

    def transliterate(self, text, normpunc=False, ligatures=False):
        tokens = self.cedict.tokenize(text)
        ipa_tokens = []
        for token in tokens:
            if token in self.cedict.hanzi:
                (pinyin, _) = self.cedict.hanzi[token]
                pinyin = u''.join(pinyin).lower()
                ipa = self.rules.apply(pinyin)
                ipa_tokens.append(ipa.replace(u',', u''))
            else:
                if normpunc:
                    token = self.normalize_punc(token)
                ipa_tokens.append(token)
            ipa_tokens = map(ligaturize, ipa_tokens) if ligatures else ipa_tokens
        return u''.join(ipa_tokens)


class EpihanTraditional(Epihan):
    def __init__(self, ligatures=False, cedict_file=None, rules_file='pinyin-to-ipa.txt'):
        if not cedict_file:
            raise MissingData('Please specify a location for the CC-CEDict file.')
        rules_file = os.path.join('data', 'rules', rules_file)
        rules_file = pkg_resources.resource_filename(__name__, rules_file)
        self.cedict = cedict.CEDictTrie(cedict_file, traditional=True)
        self.rules = rules.Rules([rules_file])
