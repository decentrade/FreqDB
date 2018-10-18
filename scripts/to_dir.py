#!/usr/bin/python
#coding: utf8

from __future__ import unicode_literals
from collections import Counter
import os, codecs
import sqlite3, sys
if not sys.argv[2:]: raise Exception("Usage: python to_dir.py rus eng")
if not os.path.isdir(sys.argv[1]): os.mkdir(sys.argv[1])

EXCLUDE_SRC = ('3546',)

con = sqlite3.connect('panlex_lite/db.sqlite')
lemmas = []
src = codecs.open(sys.argv[1]+'.txt','r','utf8')
src_lang = con.execute('SELECT id FROM langvar WHERE lang_code=?',(sys.argv[1],)).fetchone()[0]
dst_lang = con.execute('SELECT id FROM langvar WHERE lang_code=?',(sys.argv[2],)).fetchone()[0]
if sys.argv[3:]:
 dst_lang = con.execute('SELECT id FROM langvar WHERE lang_code=? ANV var_code=?',(sys.argv[2],int(sys.argv[3]))).fetchone()[0]
print 'Translating lang', src_lang, 'to', dst_lang
sys.stdout.flush()
for s in src:
 s = s.strip()
 #l = con.execute('SELECT ee.txt, t.source FROM expr e JOIN denotationx d ON d.expr=e.id JOIN denotationx t ON t.meaning=d.meaning JOIN expr ee ON t.expr=ee.id JOIN source s ON t.source = s.id \
 # WHERE s.label like "'+'-'.join(sys.argv[1:])+'%" AND t.langvar=? AND e.langvar=? AND e.txt=? AND t.source NOT IN ({}) ORDER BY t.source'.format(','.join(EXCLUDE_SRC)),(dst_lang, src_lang, s)).fetchall()
 #if not l: 
 l = con.execute('SELECT ee.txt, t.source FROM expr e JOIN denotationx d ON d.expr=e.id JOIN denotationx t ON t.meaning=d.meaning JOIN expr ee ON t.expr=ee.id JOIN source s ON t.source = s.id \
  WHERE t.langvar=? AND e.langvar=? AND e.txt=?',(dst_lang, src_lang, s)).fetchall()
 if not l:
  print 'dismiss', s
  sys.stdout.flush()
  lemmas.append('')
 else:
  ss = l[0][1]
  #x = '; '.join(set([ll[0] for ll in l if ll[1] == ss]))
  xx = Counter(zip(*l)[0]).most_common(5)
  c1 = int(xx[0][1]/2)
  xx = [x[0] for x in xx if x[1] >= c1 and x[0] != s]
  x = '; '.join(xx)
  lemmas.append(x)
  print s, '=>', x
  sys.stdout.flush()

outf = '-'.join(sys.argv[2:])
codecs.open(sys.argv[1]+outf+'.txt','w','utf8').write('\n'.join(lemmas).rstrip())
