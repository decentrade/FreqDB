# FreqDB
Word frequency lists for FreqVocab android\ios flashcard app.

The lists are in text format(gzipped), one word per line.
All words are in normal forms.
For example, for English languge, words are given in ```eng.txt```. 
Definitions for the same words in English are in ```engeng.txt```.
Translations of the same words to Russian are in ```engrus.txt``` and so on.

The lists are sorted by the word frequency in the Wikipedia dump for corresponding language.

Scripts used to make lists are in ```scripts``` directory. 
Run them using ```make``` or ```make <lang>```(see Makefile for the list of targets).
I've included sqlite databases with exact count of each word in the Wikipedia dump and part of speech tags.
If you want to rebuild that databases, install the following python modules for correct word segmentation and normalization:
For Chineese language ```jieba``` pip module must be installed.
For Russian language ```pymorphy``` and ```pymorphy-dicts``` pip modules must be installed.
For all the rest languages ```spacy``` pip\conda (conda recommended) module must be installed with [corresponding language model](https://spacy.io/usage/models).
