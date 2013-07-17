# -*- coding: utf-8 -*-

import nltk
import pymorphy2
import codecs
import re

Morph = pymorphy2.MorphAnalyzer()
FinalSentence = []
ListLen = []
VisibleText = []

"""
----- Creating list of lexical minimum -----
"""


def LexicalMinimumList(LexicalMinimumListFileName):
    LexicalMinimum = []

    fp = open(LexicalMinimumListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        LexicalMinimum.append(word)
        line = fp.readline()
    fp.close()
    return LexicalMinimum

"""
----- Sentences tokenization -----
Text from file -> list of sentences
"""


def SentenceCutter(FullText):
    ListofSentences = nltk.PunktSentenceTokenizer().tokenize(FullText)
    for s in ListofSentences:
        WordCutter(s)

"""
----- Words tokenization -----
List of sentences -> List of words
"""


def WordCutter(Sentence):
    ListofWords = nltk.WordPunctTokenizer().tokenize(Sentence)
    a = len(ListofWords)
    ListLen.append(a)
    for w in ListofWords:
        Lemmatization(w)

    SentenceChecker(FinalSentence)

    del FinalSentence[:]
    return

"""
----- Lemmatization -----
Word from list of words -> ["word", "POS", "lemma"]
"""


def Lemmatization(Word):
    WordObject = []
    WordObject.append(Word)
    Word = Word.lower()
    try:
        WordinWork = Morph.parse(Word)[0]
        WordObject.append(WordinWork.tag.POS)
        WordObject.append(WordinWork.normal_form)
        FinalSentence.append(WordObject)
    except IndexError:
        return

"""
----- Checking sentence -----
Lemma -> yes/no
If no, then count += 1
"""


def SentenceChecker(Sentence):
    OneSent = []
    count = 0
    for OneWord in Sentence:
        if OneWord[2] in LexicalMinimum:
            if OneWord[0] == "," or OneWord[0] == "." or OneWord[0] == ":" or OneWord[0] == ";" or OneWord[0] == "!" or OneWord[0] == "?" or OneWord[0] == "-":
                OneSent.append(OneWord[0])
            else:
                OneSent.append(' ' + '<span class="correctWord">' + OneWord[0] + '</span>')        
        else:            
            OneSent.append(' ' + '<span class="wrongWord">' + OneWord[0] + '</span>')
            count += 1
    
    x = ListLen[-1]*0.33
    if count > x:
        OneSent.insert(0, '<span class="Complex sentence">')
    else:
        OneSent.insert(0, '<span class="Simple sentence">')
    OneSent.append('</span>')
    
    VisibleText.append(OneSent)

"""
----- Data -----
"""


LexMin = codecs.open('Data/lexmin.txt', 'r', 'utf-8')
LexicalMinimum = LexMin.read()

TextFile = codecs.open('Data/corpus.txt', 'r', 'utf-8')
Text = TextFile.read()

#For loading data from file please uncomment and edit following strings
#import csv
#Text = csv.reader(open('Data/file.csv', 'rb'), delimiter='', quotechar = '')

SentenceCutter(Text)

for element in VisibleText:
    for e in element:
        print e

