#!/usr/bin/python
#coding: utf-8
from __future__ import unicode_literals
import codecs, sys, glob, json, re, os.path
from collections import Counter

START=0

skip_pos = set(['PUNCT','SYM','NUM','PROPN','INTJ'])
def count_conll(conll):
  for sp in conll:
    if len(sp) != 7: continue
    n, w, norm, pos, tags, root, l = sp
    if not norm: continue
    if pos in skip_pos: continue
    if '_' in w: continue
    if '_' in norm: continue
    if not norm.isalpha(): continue
    yield norm + '/' + pos

def save():
 import sqlite3
 con = sqlite3.connect(sys.argv[1]+'.db')
 con.execute('DROP TABLE IF EXISTS lemma')
 con.execute('CREATE TABLE lemma(word text, count integer)')
 con.commit()

 print 'Saving', len(all_cnt)
 con.executemany('INSERT INTO lemma(word, count) VALUES (?,?)', all_cnt.most_common())
 con.commit()
 con.close()

def load():
 if not os.path.isfile(sys.argv[1]+'.db'): return Counter()
 import sqlite3
 con = sqlite3.connect(sys.argv[1]+'.db')
 return Counter(dict(con.execute('SELECT * FROM lemma')))
 
all_cnt = load()
print 'Loaded', len(all_cnt)

if __name__ == '__main__':
 try:
  if not sys.argv[1:]: raise Exception("Usage: python count_lemmas.py ru")
  lang = __import__(sys.argv[1])
  i = 0
  cnt = Counter()
  for line in codecs.getreader('utf-8')(sys.stdin):
     i += 1
     if i < START: continue
     if i % 30000 == 0: lang.reinit()
     if i % 100 == 0:
      all_cnt.update(cnt)
      cnt = Counter()
      save()
     print i
     sys.stdout.flush()
     
     if not line.strip(): continue
     if line.startswith('#'): continue
     if len(line) < 2000: continue
     try: text = json.loads(line)['text'].replace('<br>','\n').replace('<br/>','\n')
     except:
      print 'error parsing json in line', i
      continue
     text = text.strip().replace('«','"').replace('»','"').replace('”','"').replace('“','"')
     text = text.replace("<",'').replace('>','').replace('...','…')
     text = text.replace('“','"').replace('”','"').replace('¬','').replace('­','').replace('=','равно')
     text = text.replace(u'\x01',' ').replace(' ',' ').replace('–','-').replace('—','-').replace('--','-')
     for l in lang.tokenize(text).split('\n'):
       l = l.strip()
       if not l: continue
       #sys.stdout.write('.')
       #sys.stdout.flush()
       #print l
       cnt.update(Counter(count_conll(lang.parse(l))))
     
 except KeyboardInterrupt: pass
 save()
