#!/usr/bin/pypy
#coding: utf8

from __future__ import unicode_literals
from collections import Counter
import os, codecs
import sys
if not sys.argv[1:]: raise Exception("Usage: python find_similar.py engeng")

def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    return answer

src = codecs.open(sys.argv[1]+'.txt','r','utf8').read().split('\n')
wrd = codecs.open(sys.argv[1][:3]+'.txt','r','utf8').read().split('\n')

dst = []

for s, w in zip(src, wrd):
    if not s or len(w) < 6:
        dst.append(s)
        continue
    comm = longestSubstringFinder(s.lower(),w.lower())
    if len(comm) > len(w)/2: 
        print w, s.lower().split(comm)[0], '(', comm, ')', s.lower().split(comm)[1]
        dst.append('')
        continue
    dst.append(s)

codecs.open(sys.argv[1]+'.txt','w','utf8').write('\n'.join(dst).strip())
