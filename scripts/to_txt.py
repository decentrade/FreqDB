#!/usr/bin/python
#coding: utf8

from __future__ import unicode_literals
import sqlite3, sys, codecs, os
if not sys.argv[2:]: raise Exception("Usage: python to_txt.py rus/ru.db rus")

con = sqlite3.connect('panlex_lite/db.sqlite')
src = sqlite3.connect(sys.argv[1])
wkt = None
if os.path.isfile('wikt/'+sys.argv[2]+'.db'):
 wkt = sqlite3.connect('wikt/'+sys.argv[2]+'.db')

src_lang = con.execute('SELECT id FROM langvar WHERE lang_code=?',(sys.argv[2],)).fetchone()[0]
print 'Filtering for', src_lang

lemmas = src.execute('SELECT * from lemma').fetchall()
ll = set(zip(*lemmas)[0])
ll = set([x.split('/')[0] for x in ll])
ll |= set([x.replace('ё','е') for x in ll])
wl = set([])
if wkt:
 wl = wkt.execute('SELECT name from word').fetchall()
 wl = set(zip(*wl)[0])
pl = con.execute('SELECT txt FROM expr WHERE langvar=? AND txt NOT LIKE "% %"',(src_lang,)).fetchall()
pl = set(zip(*pl)[0])
print 'lemmas', len(ll), 'panlex', len(pl), 'wikt', len(wl)

fl = ll&(pl|wl)
print 'filtered', len(fl)

wl=set([x for x in wl if x.isalpha() and x.islower() and not x.endswith('вший')])-fl
pl=set([x for x in pl if x.isalpha() and x.islower() and not x.endswith('вший')])-fl-wl
print 'from panlex', len(pl), 'from wikt', len(wl)

import uniout
print 'from panlex', list(pl)[:10]
print 'from wikt', list(wl)[:10]
print 'dismiss', [(w,c) for w,c in lemmas if w.split('/')[0] not in fl][:10]
all_dst = [w.split('/')[0] for w,c in lemmas if w.split('/')[0] in fl]+list(wl)+list(pl)
codecs.open(sys.argv[2]+'.txt','w','utf8').write('\n'.join(all_dst))

try:
 all_dst = [w.split('/')[1] for w,c in lemmas if w.split('/')[0] in fl]
 codecs.open(sys.argv[2]+'.pos','w','utf8').write('\n'.join(all_dst))
except: pass
