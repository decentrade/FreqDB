models_dir = Chinese Spanish-AnCora English Hindi Arabic Portuguese Russian-SynTagRus German French Italian Polish Romanian Dutch Greek Hungarian Czech Swedish Finnish-FTB Hebrew Kazakh Turkish Persian Tamil Indonesian

all: engeng.txt rusrus.txt cmn spa eng deu rus fra por ita nld
	gzip *.txt

clean:
	rm -rf *.bz2 *.txt *.gz

panlex_lite.zip:
	wget http://dev.panlex.org/db/panlex_lite.zip

panlex_lite: panlex_lite.zip
	unzip panlex_lite.zip

filter:
	pypy scripts/filter.py *rus.txt
	pypy scripts/filter_en.py *eng.txt

$(models_dir):
	wget http://download.tensorflow.org/models/parsey_universal/$@.zip
	unzip $@.zip
	rm $@.zip

ud-treebanks-v2.2:
	wget https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2837/ud-treebanks-v2.2.tgz?sequence=1&isAllowed=y
	tar xzf ud-treebanks-v2.2.tgz*

wikiextractor:
        git clone https://github.com/attardi/wikiextractor.git

wiktionary:
	git clone https://github.com/ainy/wiktionary

wikt: wiktionary
	$(MAKE) -C wiktionary
	mkdir wikt

wikt/eng.db: wikt
	cp wiktionary/enwikt.db wikt/eng.db

engeng.txt: wikt/eng.db eng
	python to_wikt.py eng

wikt/rus.db: wikt
	cp wiktionary/wiki.db wikt/rus.db

rusrus.txt: wikt/rus.db rus
	python to_wikt_extract.py rus

zh:Chinese cmn
zhwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2
zh.db: wikiextractor zhwiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - zhwiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py zh
cmn: panlex_lite zh.db
	python to_txt.py zh.db cmn
	for i in spa eng deu rus fra por ita jpn arb uig;do pypy to_dir.py cmn $$i;done

coverage:
	python coverage.py es.db spa.txt
	python coverage.py de.db deu.txt
	python coverage.py fr.db fra.txt
	python coverage.py pt.db por.txt
	python coverage.py it.db ita.txt
	python coverage.py nl.db nld.txt

es:Spanish-AnCora spa
eswiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/eswiki/latest/eswiki-latest-pages-articles.xml.bz2
es.db: wikiextractor eswiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - eswiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py es
spa: panlex_lite es.db
	python to_txt.py es.db spa
	for i in eng deu rus fra por ita jpn arb;do pypy to_dir.py spa $$i;done

en:English eng
enwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
en.db: wikiextractor enwiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - enwiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py en
eng: panlex_lite en.db
	python to_txt.py en.db eng
	for i in spa deu rus fra por ita jpn arb;do pypy to_dir.py eng $$i;done

de: German deu
dewiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/dewiki/latest/dewiki-latest-pages-articles.xml.bz2
de.db: wikiextractor dewiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - dewiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py de
deu: panlex_litede.db
	python to_txt.py de.db deu
	for i in spa eng rus fra por ita jpn arb;do pypy to_dir.py deu $$i;done

ru:Russian-SynTagRus rus
ruwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/ruwiki/latest/ruwiki-latest-pages-articles.xml.bz2
ru.db: wikiextractor Russian-SynTagRus ruwiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - ruwiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py ru
rus: panlex_literu.db
	python to_txt.py ru.db rus
	for i in spa eng deu fra por ita jpn arb;do pypy to_dir.py rus $$i;done

fr: French fra
frwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/frwiki/latest/frwiki-latest-pages-articles.xml.bz2
fr.db: wikiextractor frwiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - frwiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py fr
fra: panlex_litefr.db
	python to_txt.py fr.db fra
	for i in spa eng deu rus por ita jpn arb;do pypy to_dir.py fra $$i;done

pt:Portuguese por
ptwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/ptwiki/latest/ptwiki-latest-pages-articles.xml.bz2
pt.db: wikiextractor ptwiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - ptwiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py pt
por: panlex_lite pt.db
	python to_txt.py pt.db por
	for i in spa eng deu rus fra ita jpn arb;do pypy to_dir.py por $$i;done

it: Italian ita
itwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/itwiki/latest/itwiki-latest-pages-articles.xml.bz2
it.db: wikiextractor itwiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - itwiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py it
ita: panlex_liteit.db
	python to_txt.py it.db ita
	for i in spa eng deu rus fra por jpn arb;do pypy to_dir.py ita $$i;done

nl: Dutch nld
nlwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/nlwiki/latest/nlwiki-latest-pages-articles.xml.bz2
nl.db: wikiextractor nlwiki-latest-pages-articles.xml.bz2
	python wikiextractor/WikiExtractor.py --json -o - nlwiki-latest-pages-articles.xml.bz2 | python count_lemmas_pipe.py nl
nld: panlex_lite nl.db
	python to_txt.py nl.db nld
	for i in spa eng deu rus fra por ita jpn arb;do pypy to_dir.py nld $$i;done

plwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/plwiki/latest/plwiki-latest-pages-articles.xml.bz2
pl: Polish plwiki-latest-pages-articles.xml.bz2

rowiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/rowiki/latest/rowiki-latest-pages-articles.xml.bz2
ro: Romanian rowiki-latest-pages-articles.xml.bz2

elwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/elwiki/latest/elwiki-latest-pages-articles.xml.bz2
el: Greek elwiki-latest-pages-articles.xml.bz2

huwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/huwiki/latest/huwiki-latest-pages-articles.xml.bz2
hu: Hungarian huwiki-latest-pages-articles.xml.bz2

cswiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/cswiki/latest/cswiki-latest-pages-articles.xml.bz2
cs: Czech cswiki-latest-pages-articles.xml.bz2

svwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/svwiki/latest/svwiki-latest-pages-articles.xml.bz2
sv: Swedish svwiki-latest-pages-articles.xml.bz2

fiwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/fiwiki/latest/fiwiki-latest-pages-articles.xml.bz2
fi: Finnish-FTB fiwiki-latest-pages-articles.xml.bz2

hewiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/hewiki/latest/hewiki-latest-pages-articles.xml.bz2
he: Hebrew hewiki-latest-pages-articles.xml.bz2

kkwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/kkwiki/latest/kkwiki-latest-pages-articles.xml.bz2
kk: Kazakh kkwiki-latest-pages-articles.xml.bz2

trwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/trwiki/latest/trwiki-latest-pages-articles.xml.bz2
tr: Turkish trwiki-latest-pages-articles.xml.bz2

tawiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/tawiki/latest/tawiki-latest-pages-articles.xml.bz2
ta: Tamil tawiki-latest-pages-articles.xml.bz2

idwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/idwiki/latest/idwiki-latest-pages-articles.xml.bz2
id: Indonesian idwiki-latest-pages-articles.xml.bz2

hiwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/hiwiki/latest/hiwiki-latest-pages-articles.xml.bz2
hi: Hindi hiwiki-latest-pages-articles.xml.bz2

arwiki-latest-pages-articles.xml.bz2:
	wget https://dumps.wikimedia.org/arwiki/latest/arwiki-latest-pages-articles.xml.bz2
ar: Arabic arwiki-latest-pages-articles.xml.bz2

