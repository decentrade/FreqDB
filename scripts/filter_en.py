#!/usr/bin/env pypy
#coding: utf-8
from __future__ import unicode_literals
import sys, codecs, re
if not sys.argv[1:]: raise Exception('Usage: pypy ru_filter.py rus.txt ruseng.txt')

task = set(
''''''.split('\n')
)
contain = [
    'fuck',
    'bullshit',
    'menstr',
    'mastur',
    'genital'
]
obscene=set('''shit
asshole
dick
dickhead
cunt
boob
boobs
dildo
crap'''.split('\n'))

import glob
lemmas = [codecs.open(x,'r','utf8').readlines() for x in sys.argv[1:]]
for k,l in zip(sys.argv[1:],lemmas):
 filtered = 0
 ll = len(l)
 print 'filtering', k[:3]
 lang = [codecs.open(x,'r','utf8').readlines() for x in glob.glob(k[:3]+'*.txt')]
 for i,w in enumerate(l[::-1]):
  ww = w.strip().split('; ')
  if any([c in w for c in contain]) or any([www in obscene for www in ww]):
   print 'dismiss', w,
   filtered += 1
   try:
       for f in lang: del f[ll-i-1]
   except: pass

 print 'filtered', filtered
 print [codecs.open(x,'w','utf8').write(''.join(l)) for l,x in zip(lang,glob.glob(k[:3]+'*.txt'))]
print