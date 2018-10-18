#coding:utf-8
from __future__ import unicode_literals
import uniout
import codecs, sys, glob
#import dawg_python as dawg
#import dawg
import re
import jieba


skip_pos = set(['PUNCT','SYM','NUM','X'])
punct = set([u'、', u'！', u'。', u'̄', u'─', u'）', u'（', u'》', u'《', u'」', u'，', u'』', u'『', u"'", u'〕', u'〔', u'’', u'‘', u'；', u'：', u'”', u'“', u'？', u'!', u'"', u'‧', u')', u'(', u'-', u',', u'/', u'.', u'〉', u'·', u'〈', u';', u':', u'?', u'丶', u'「', u'•', u'／', u'@', u'・', u'~'])
sym = punct|set([u'+', u'.', u'°', u'/', u'＋', u'$',u'─', u"''", u'.', u'—', u'.', u'`', u'-', u'…', u'⋯', u'.', u'-', u'.','(',')'])
num = re.compile(r'[0-9十]')
X = re.compile(r'[a-zA-Z]')


def reinit(): pass

def pos(w):
 if any([x in sym for x in w]): return 'SYM'
 if num.match(w): return 'NUM'
 if X.match(w): return 'X'
 return ''

parse = lambda s: [(i, w, w, pos(w), [], 0, '') for i,w in enumerate(s.split())]
tokenize = lambda s: ' '.join(jieba.cut(s))

def _tokenize(s):
 i = 0
 while i < len(s):
  p = pos(s[i])
  w = s[i]
  while i+1<len(s) and pos(s[i+1])==p:
    i += 1;w += s[i]
  i += 1
  if p:
   yield w
   continue
  while w:
   x = zh.prefixes(w)
   if not x: x = [w[0]]
   w = w[len(x[-1]):]
   yield x[-1]

if __name__ == '__main__':
 err = 0
 total = 0
 expect = []
 text = []
 for loc in glob.glob("ud-treebanks-v2.2/UD_Chinese-*/*.conllu"):
  print 'Processing', loc
  for line in codecs.open(loc, 'r','utf-8'):
    if not line.strip(): continue
    if line.startswith('# text = '):
     text.append(line[9:])
     continue
    if line.startswith('#'):continue
    sp = line.split('\t')
    if len(sp) != 10: continue
    w = sp[1]
    expect.append(w)
 got = ' '.join([tokenize(t) for t in text]).split()
 print 'Checking...'
 while got and expect:
    gw = got.pop(0)
    ew = expect.pop(0)
    if gw != ew:
       err += 1
       #print 'got', gw, 'expect', ew
       while gw != ew:
        if ew.startswith(gw): gw+=got.pop(0)
        elif gw.startswith(ew): ew+=expect.pop(0)
        else: raise 'OMFG!'
    total += 1
 print float(err) / float(total)

