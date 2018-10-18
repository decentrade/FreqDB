#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals
import spacy

LANG = 'pt'
DISABLE = ['parser']

nlp = spacy.load(LANG, disable=DISABLE)
convert = {}
tokenize = lambda x:x.replace('\n','').replace('.','.\n')
parse = lambda x:list(_parse(x))

def reinit():
 global nlp
 nlp = spacy.load(LANG, disable=DISABLE)
 

def _parse(x):
 global nlp
 
 for t in nlp(x):
    #if not t.lemma_.isalpha(): continue
    if t.lemma_ in convert: t.lemma_=convert[t.lemma_]
    if t.ent_type_: t.lemma_=''
    yield t.i, t.text, t.lemma_, t.pos_, [], 0, ''


if __name__ == '__main__':pass


