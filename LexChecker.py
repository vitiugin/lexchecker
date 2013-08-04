#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
LIB64_DIR = '/home/k/karpnv/lib64/python2.7/site-packages'
sys.path.insert(0, LIB64_DIR)

import pymorphy2
import nltk
import urllib


class LexChecker(object): 


    def __init__(self):
        self.Morph = pymorphy2.MorphAnalyzer()
        self.FinalSentence = []
        self.ListLen = []
        self.VisibleText = []
        self.LexicalMinimum = urllib.urlopen('https://raw.github.com/fedorvityugin/lexchecker/master/Data/lexmin_basic.txt').read().decode('utf-8')
        self.LexicalMinimum = self.LexicalMinimum + urllib.urlopen('https://raw.github.com/fedorvityugin/lexchecker/master/Data/lexmin_elementary.txt').read().decode('utf-8')

    """
    ----- Creating list of lexical minimum -----
    """

    def LexicalMinimumList(self,LexicalMinimumListFileName):
        lexicalMinimum = []
    
        fp = open(LexicalMinimumListFileName, 'r')
        line = fp.readline().encode('utf-8')
        while line:
            word = line.strip()
            lexicalMinimum.append(word)
            line = fp.readline().encode('utf-8')
        fp.close()
        return lexicalMinimum

    """
    ----- Sentences tokenization -----
    Text from file -> list of sentences
    """


    def SentenceCutter(self, FullText):
        ListofSentences = nltk.PunktSentenceTokenizer().tokenize(FullText)
        for s in ListofSentences:
            self.WordCutter(s)

    """
    ----- Words tokenization -----
    List of sentences -> List of words
    """

    def WordCutter(self,Sentence):
        ListofWords = nltk.WordPunctTokenizer().tokenize(Sentence)
        a = len(ListofWords)
        self.ListLen.append(a)
        for w in ListofWords:
            self.Lemmatization(w)

        self.SentenceChecker(self.FinalSentence)

        del self.FinalSentence[:]
        return

    """
    ----- Lemmatization -----
    Word from list of words -> ["word", "POS", "lemma"]
    """

    def Lemmatization(self,Word):
        WordObject = []
        WordObject.append(Word)
        Word = Word.lower()
        try:
            WordinWork = self.Morph.parse(Word)[0]
            WordObject.append(WordinWork.tag.POS)
            WordObject.append(WordinWork.normal_form)
            self.FinalSentence.append(WordObject)
        except IndexError:
            return

    """
    ----- Checking sentence -----
    Lemma -> yes/no
    If no, then count += 1
    """


    def SentenceChecker(self,Sentence):
        OneSent = []
        count = 0
        for OneWord in Sentence:
            if OneWord[2] in self.LexicalMinimum:
                if OneWord[0] == "," or OneWord[0] == "." or OneWord[0] == ":" or OneWord[0] == ";" or OneWord[0] == "!" or OneWord[0] == "?" or OneWord[0] == "-":
                    OneSent.append(OneWord[0])
                else:
                    OneSent.append(' ' + '<span class="correctWord">' + OneWord[0] + '</span>')        
            else:            
                OneSent.append(' ' + '<span class="wrongWord">' + OneWord[0] + '</span>')
                count += 1
    
        x = self.ListLen[-1]*0.33
        if count > x:
            OneSent.insert(0, '<span class="Complex sentence">')
        else:
            OneSent.insert(0, '<span class="Simple sentence">')
        OneSent.append('</span>')
    
        self.VisibleText.append(OneSent)
