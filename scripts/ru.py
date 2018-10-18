#coding: utf-8
from __future__ import unicode_literals
from subprocess import Popen, PIPE, STDOUT
import os.path, re
MODELS_PATH = os.path.abspath(os.path.dirname(__file__))
LEMMAS_PATH = MODELS_PATH+'/lemmas.txt'
REPLACE_ABBR = True

p = Popen(['bash', MODELS_PATH+'/parsey_universal/parse.sh', MODELS_PATH+'/Russian-SynTagRus'], stdout=PIPE, stdin=PIPE, stderr=open('syntaxnet.log', 'w'))

def reinit(): pass

def _parse(s):
  p.stdin.write((s +'\n').encode('utf-8'))
  while True: 
    x = p.stdout.readline().rstrip()
    if not x: break
    yield x.decode('utf-8').split('\t')[:8]

tconv = {'actv':'Voice=Act', 'indc':'Mood=Ind', 'gen2':'Case=Par', 'datv':'Case=Dat', 'accs':'Case=Acc','acc2':'Case=Acc', 'ANim':'Animacy=Anim','anim':'Animacy=Anim', 'perf':'Aspect=Perf', 'plur':'Number=Plur', 'femn':'Gender=Fem', 'impf':'Aspect=Imp', 'pssv':'Voice=Pass', 'inan':'Animacy=Inan', 'sing':'Number=Sing', 'past':'Tense=Past', 'neut':'Gender=Neut', 'pres':'Tense=Pres', 'voct':'Case=Voc', 'nomn':'Case=Nom', 'futr':'Tense=Fut', 'Supr':'Degree=Sup', '2per':'Person=2', '3per':'Person=3', 'impr':'Mood=Imp', '1per':'Person=1', 'ablt':'Case=Ins', 'gent':'Case=Gen','gen1':'Case=Gen', 'masc':'Gender=Masc', 'loct':'Case=Loc', 'loc2':'Case=Loc', 'loc1':'Case=Loc'}

pconv = {
  "ADJF":["ADJ"],
  "ADJS":["ADJ","Variant=Brev"],
  "COMP":["ADJ","Degree=Cmp"],
  "VERB":["VERB","VerbForm=Fin"],
  "INFN":["VERB","VerbForm=Inf"],
  "PRTF":["VERB","VerbForm=Part"],
  "PRTS":["VERB","VerbForm=Part", "Variant=Brev"],
  "GRND":["VERB","VerbForm=Trans"],
  "NUMR":["NUM"],
  "ROMN":["NUM"],
  "LATN":["NUM"],
  "NUMB":["NUM"],
  "ADVB":["ADV"],
  "NPRO":["PRON"],
  "PRED":["ADV","Degree=Pos"],
  "PREP":["ADP"],
  "PRCL":["PART"],
}

case = {
'Case=Nom', # именительный падеж  
'Case=Gen', # родительный падеж
'Case=Dat', # дательный падеж
'Case=Acc', # винительный падеж
'Case=Ins', # творительный падеж
'Case=Loc', # предложный падеж
'Case=Par', # частичный падеж: с ходу, с голоду, из виду, с краю, без разбору
}

import pymorphy2
morph = pymorphy2.MorphAnalyzer(path='dict')
def get_morph(w, pos, tags):
 try:
  for info in morph.parse(w):
    tag, n = str(info.tag), info.normal_form
    tags_guess = tag.replace(',',' ').split()
    if tags_guess[0] == 'UNKN': 
      if w.isupper():
        if all(i in 'XIV' for i in w):
          tags_guess = ['NUM']
        else:
          tags_guess = ['NOUN']
      elif w.replace(',','').replace('.','').isdigit():
        tags_guess = ['NUM']
      elif w.endswith('.'):
        tags_guess = ['NOUN']
      else:
        tags_guess = ['_']
    if n.lower()==u'который': 
      tags_guess[0] = 'ADJ'
    elif n.lower()==u'это' and tags_guess[0] == 'NPRO':
      #PRON PART DET
      tags_guess[0] = 'NOUN'
      tags_guess.append('Animacy=Inan')
    elif tag.startswith('ADJF,Apro'):
      tags_guess[0] = 'DET'
    elif tags_guess[0] == 'CONJ' and len(w) > 2:
      tags_guess[0] = 'SCONJ'
    elif tags_guess[0] in pconv:
      tags_guess = pconv[tags_guess[0]] + tags_guess[1:]
    
    if n==u'быть': 
      if tags_guess[0] == 'PRTF':
        tags_guess[0] = 'ADJ'
      else:
        tags_guess[0] = 'AUX'
        #if 'past' in tags_guess: tags_guess.append('Tense=Pres')
    
    pos_guess = tags_guess.pop(0)
    for i, tg in enumerate(tags_guess):
      if tg in tconv:
        tags_guess[i] = tconv[tg]
    
    if pos_guess in ('VERB','AUX') and not 'Voice=Pass' in tags_guess: tags_guess.append('Voice=Act') 
    if (pos_guess in ('ADV','ADJ')) and 'Degree=Pos' not in tags_guess and 'Degree=Cmp' not in tags_guess and 'Degree=Sup' not in tags_guess: tags_guess.append('Degree=Pos') 
    
    yield n, 2*(pos==pos_guess) - len(tags ^ set(tags_guess)) + info.score, tags_guess
 except:
  print 'pymorphy-error:', w, pos

def normalize(w, p, m):
  if '_' in w: 
    return w.replace('_',' ')
  if re.search('[a-zA-Z]', w): return ''
  if p in ('SYM', 'PUNCT'):
    return w
  
  m = set(m.split('|')[:-1])
  try: 
   bm = max( get_morph(w, p, m), key = lambda (n,s,m): s )
   if 'Geox' in bm[2] or 'Surn' in bm[2] or 'Patr' in bm[2] or 'Name' in bm[2]: return ''
   return bm[0]
  except:
   return ''

parse = lambda s: [(int(i)-1, w.replace('_',' '), normalize(w, p, m), p, m.split('|')[:-1], (int(h) or int(i))-1, l) for i,w,_,p,_,m,h,l in _parse(s)]

from codecs import open
lemmas = {}
for w in open(LEMMAS_PATH, 'r', 'utf-8'):
  w = w.strip()
  lemmas[w.replace('_',' ')] = w


#ADV|smth + ADP
lemmas_preps = {
'несмотря_на',
'невзирая_на',
'наравне_с',
'вплоть_до',
'тому_назад',
}

#ADP + NOUN + maybe(ADP)
lemmas_preps_ambig = {
'в_течение',
'во_время',
'с_помощью',
'в_качестве',
'за_счет',
'в_ходе',
'в_связи_с',
'в_отличие_от',
'в_виде',
'по_поводу',
'по_отношению_к',
'в_отношении',
'при_помощи',
'в_соответствии_с',
'по_сравнению_с',
'по_мере',
'за_исключением',
'во_избежание',
#'по_сравнению_со',
}

import re
splitter = re.compile(r'(\W*)(\S*?)(\W*?)\s', flags=re.U)
lemmatizer = re.compile(r'\b(%s)\b'%('|'.join(lemmas).replace('.','\.'),), flags=re.U)

lemmatize = lambda s: ' '.join(_lemmatize(s))
def _lemmatize(text):
  flag = True
  for smth in lemmatizer.split(text):
    if smth:
      if flag: 
        for s in _tokenize(smth): yield s
      else: 
        yield lemmas[smth]
    
    flag = not flag
  
tokenize = lambda s: ' '.join(_tokenize(s))
def _tokenize(text):
  if REPLACE_ABBR:
    text = re.sub(' млн\.?',r" миллион", text)
    text = re.sub(' млрд\.?',r" миллиард", text)
    text = re.sub(' трлн\.?',r" триллиард", text)
    text = text.replace(' г.', ' год').replace(' н. э.',' нашей эры').replace('См.','Смотри').replace(' гг.', ' годы')
    text = text.replace(' с. ш.', ' северной широты').replace(' ю. ш.',' южной широты').replace(' в. д.',' восточной долготы').replace(' з. д.',' западной долготы')
    text = text.replace(' и т. д.',' и так далее').replace(' и т. п.', 'и тому подобное').replace('()','')
    text = text.replace(' тыс.', ' тысяча').replace(' в.', ' век').replace(' вв.', ' века').replace(' чел.', ' человек').replace(' др.',' другие').replace(' пр.',' прочие')
    text = text.replace(' долл.',' долларов').replace(' р.',' рублей').replace(' руб.', ' рублей').replace(' мес.', ' месяц')

  for lpunct,word,rpunct in splitter.findall(text+' '):
      if len(lpunct.lstrip()):
          yield lpunct.strip()
      if len(word):
          yield word
      if len(rpunct):
        if rpunct in '.?!':
          yield rpunct+'\n'
        else:
          yield rpunct
        
translit_table = {u'Ё': 'Yo', u'Б': 'B', u'А': 'A', u'Г': 'G', u'В': 'V', u'Е': 'E', u'Д': 'D', u'З': 'Z', u'Ж': 'Zh', u'Й': 'Y', u'И': 'I', u'Л': 'L', u'К': 'K', u'Н': 'N', u'М': 'M', u'П': 'P', u'О': 'O', u'С': 'S', u'Р': 'R', u'У': 'U', u'Т': 'T', u'Х': 'H', u'Ф': 'F', u'Ч': 'Ch', u'Ц': 'Ts', u'Щ': 'Sch', u'Ш': 'Sh', u'Ы': 'Y', u'Ъ': '"', u'Э': 'E', u'Ь': "'", u'Я': 'Ya', u'Ю': 'Yu', u'б': 'b', u'а': 'a', u'г': 'g', u'в': 'v', u'е': 'e', u'д': 'd', u'з': 'z', u'ж': 'zh', u'й': 'y', u'и': 'i', u'л': 'l', u'к': 'k', u'н': 'n', u'м': 'm', u'п': 'p', u'о': 'o', u'с': 's', u'р': 'r', u'у': 'u', u'т': 't', u'х': 'h', u'ф': 'f', u'ч': 'ch', u'ц': 'ts', u'щ': 'sch', u'ш': 'sh', u'ы': 'y', u'ъ': '"', u'э': 'e', u'ь': "'", u'я': 'ya', u'ю': 'yu', u'ё': 'yo'}

def translit_ru(s):
  "russian cyrillic to latin alphabet converter"
  for k in translit_table.keys():
      s = s.replace(k,translit_table[k])
  return s

def translit_en(s):
  "latin to russian cyrillic alphabet converter"
  for k in sorted(translit_table, key=lambda x: -len(translit_table[x])):
      s = s.replace(translit_table[k],k)
  return s

if __name__ == '__main__':
  import uniout
  s= "Часто в качестве исполнителя выступает некоторый механизм (компьютер, токарный станок, швейная машина), но понятие алгоритма необязательно относится к компьютерным программам, так, например, чётко описанный рецепт приготовления блюда также является алгоритмом, в таком случае исполнителем является человек."
  print parse(s)
