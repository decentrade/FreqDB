#!/usr/bin/env python
#coding:utf-8
from __future__ import unicode_literals
import spacy

nlp = spacy.load('en', disable=['parser'])
convert = {'datum':'data', 'instal':'install'}
tokenize = lambda x:x.replace('\n','').replace('.','.\n')
parse = lambda x:list(_parse(x))



def reinit():
 global nlp
 nlp = spacy.load('en', disable=['parser'])
 

def _parse(x):
 global nlp
 
 for t in nlp(x):
    #if not t.lemma_.isalpha(): continue
    if t.lemma_ in convert: t.lemma_=convert[t.lemma_]
    if t.ent_type_: t.lemma_=''
    yield t.i, t.text, t.lemma_, t.pos_, [], 0, ''


if __name__ == '__main__':pass


