#!/usr/bin/python
#coding: utf8

from __future__ import unicode_literals
from collections import Counter
import os, codecs
import sqlite3, sys
if not sys.argv[1:]: raise Exception("Usage: python to_wikt_extract.py rus")
lang = sys.argv[1]
import re

from wikiextractor.WikiExtractor import Extractor, options
from StringIO import StringIO
options.write_json = True
options.expand_templates = False
e = Extractor(0,0,'','')
import json

con = sqlite3.connect('wikt/'+lang+'.db')
lemmas = []
src = codecs.open(sys.argv[1]+'.txt','r','utf8')
for s in src:
 e = Extractor(0,0,'','')

 s = s.strip()
 l = con.execute('SELECT def.def FROM def JOIN word ON word.rowid=def.word \
  WHERE word.name=?',(s,)).fetchall()
 if not l:
  print 'dismiss', s
  lemmas.append('')
 else:
  xx = ''
  for ll in l:
   x = ll[0]
   if x.startswith("''") and x[3]!="'":
     x = '"'.join(x.split("''")[2:]).strip()
     #print '0',x
   e.text = x
   o = StringIO()
   e.extract(o)
   x = json.loads(o.getvalue())['text'].strip()
   if len(x) > 150: x = x.split('.')[0]
   if len(x) > 150: continue
   #if s=='же': print '1',x
   if not x or len(x) < 3: continue
   #if not shortest or len(x) < len(shortest): shortest = x
   xx=x
   break
  xx = re.sub(r'\A\W+', '', xx, 0, re.UNICODE)
  #if xx.startswith(','): xx = xx[1:]
  lemmas.append(xx)
  print s, '=>', xx

outf = '-'.join(sys.argv[1:])
codecs.open(sys.argv[1]+outf+'.txt','w','utf8').write('\n'.join(lemmas).rstrip())
