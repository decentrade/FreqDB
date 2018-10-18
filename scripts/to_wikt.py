#!/usr/bin/python
#coding: utf8

from __future__ import unicode_literals
from collections import Counter
import os, codecs
import sqlite3, sys
if not sys.argv[1:]: raise Exception("Usage: python to_wikt.py rus")
lang = sys.argv[1]
import re
from itertools import izip

repeat = set([])
con = sqlite3.connect('wikt/'+lang+'.db')
all_pos = {}
first10 = set()
try:
 a = con.execute('select pos from def group by pos order by -count(*)').fetchall()
 first10 = set([x for (x,) in a[:10]])
 all_pos = dict([(x,str(i)+'~') for i,(x,) in enumerate(a)])
except: pass

lemmas = []
src = codecs.open(sys.argv[1]+'.txt','r','utf8').read().split('\n')
pos = src
if os.path.isfile(sys.argv[1]+'.pos'):
 pos = codecs.open(sys.argv[1]+'.pos','r','utf8').read().split('\n')

pos = pos + ['']*(len(src)-len(pos))
assert len(src) == len(pos)
conv= {
'eng':{
'ADV': 'Adverb',
'NOUN': 'Noun',
'ADP': 'Preposition',
'DET': 'Article',
'PRON': 'Pronoun',
'CCONJ': 'Conjuction',
'ADJ': 'Adjective',
'VERB': 'Verb'
}
}
conv = conv.get(sys.argv[1], conv['eng'])
for s,p in izip(src,pos):
 s = s.strip()
 p = conv.get(p.strip())
 l = con.execute('SELECT def.* FROM def JOIN word ON word.rowid=def.word \
  WHERE word.name=?',(s,)).fetchall()
 if not l:
  print 'dismiss', s
  lemmas.append('')
 else:
  xx = ''
  yy = ''
  zz = ''
  for ll in l:
   x = ll[-1].replace("''","").replace('[[','').replace(']]','')
   if s in x: continue
   if '{{' in x: continue
   if '}}' in x: continue
   if 'id=' in x: continue
   if len(x) > 150: continue
   if not x or len(x) < 3: continue
   key = x+s.lower()
   if key in repeat: continue
   repeat.add(key)
   pp = ll[1]
   x = all_pos.get(pp, '') + x
   xx = xx or x
   if ll[1] == p:
    yy = yy or x
    break
   if ll[1] in first10: zz = zz or x
  yy = (yy or zz or xx).replace('``','')
  
  lemmas.append(yy)
  print s, '=>', yy

outf = '-'.join(sys.argv[1:])
codecs.open(sys.argv[1]+outf+'.txt','w','utf8').write('\n'.join(lemmas).rstrip())
