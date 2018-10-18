#!/usr/bin/env python
#coding:utf-8

from __future__ import unicode_literals
import sqlite3,sys,codecs
import numpy as np

if not sys.argv[1:]: raise Exception('Usage: python coverage.py rus/ru.db [rus.txt]')
con = sqlite3.connect(sys.argv[1])
x = np.array(con.execute('SELECT word,count FROM lemma;').fetchall())

x,y=x.T
print 'unfiltered sizes', x.shape, y.shape
x = np.array([xx.split('/')[0] for xx in x])

if sys.argv[2:]:
 s = set(codecs.open(sys.argv[2],'r','utf-8').read().split('\n'))
 xx = np.array([i in s for i in x])
 x = x[xx]
 y = y[xx]
 print 'filtered', x.shape, y.shape

y=y.astype(int)
xx=100*y.cumsum()/y.sum()
print 'sum', y.sum()

l = len(xx)
print 'length', l

x = np.linspace(0,np.log(l),l)
xxx = xx[np.exp(x).astype(int)-1]
print list(reversed(np.polyfit(x, xxx, 7).tolist()))
