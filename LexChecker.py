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
        self.morph = pymorphy2.MorphAnalyzer()
        self.final_sentence = []
        self.len_list = []
        self.visible_text = []
        self.lexical_minimum = urllib.urlopen('https://raw.github.com/fedorvityugin/lexchecker/master/Data/lexmin_basic.txt').read().decode('utf-8')
        self.lexical_minimum = self.lexical_minimum + urllib.urlopen('https://raw.github.com/fedorvityugin/lexchecker/master/Data/lexmin_elementary.txt').read().decode('utf-8')
        self.lexical_minimum = self.lexical_minimum + urllib.urlopen('https://raw.github.com/fedorvityugin/lexchecker/master/Data/lexmin_first.txt').read().decode('utf-8')

    """
    ----- Creating list of lexical minimum -----
    """

    def open_lex_min_list(self,lex_min_list_file_name):
        lexical_minimum = []
    
        fp = open(lex_min_list_file_name, 'r')
        line = fp.readline().encode('utf-8')
        while line:
            word = line.strip()
            lexical_minimum.append(word)
            line = fp.readline().encode('utf-8')
        fp.close()
        return lexical_minimum

    """
    ----- Sentences tokenization -----
    Text from file -> list of sentences
    """


    def cut_sentence(self, full_text):
        list_of_sentences = nltk.PunktSentenceTokenizer().tokenize(full_text)
        for s in list_of_sentences:
            self.cut_words(s)

    """
    ----- Words tokenization -----
    List of sentences -> List of words
    """

    def cut_words(self,sentence):
        list_of_words = nltk.WordPunctTokenizer().tokenize(sentence)
        a = len(list_of_words)
        self.len_list.append(a)
        for w in list_of_words:
            self.lemmatise(w)

        self.check_sentence(self.final_sentence)

        del self.final_sentence[:]
        return

    """
    ----- Lemmatization -----
    Word from list of words -> ["word", "POS", "lemma"]
    """

    def lemmatise(self,word):
        word_object = []
        word_object.append(word)
        word = word.lower()
        try:
            word_in_work = self.morph.parse(word)[0]
            word_object.append(word_in_work.tag.POS)
            word_object.append(word_in_work.normal_form)
            self.final_sentence.append(word_object)
        except IndexError:
            return

    """
    ----- Checking sentence -----
    Lemma -> yes/no
    If no, then count += 1
    """


    def check_sentence(self,sentence):
        one_sent = []
        count = 0
        for one_word in sentence:
            if one_word[2] in self.lexical_minimum:
                if one_word[0] == "," or one_word[0] == "." or one_word[0] == ":" or one_word[0] == ";" or one_word[0] == "!" or one_word[0] == "?" or one_word[0] == "-":
                    one_sent.append(one_word[0])
                else:
                    one_sent.append(' ' + '<span class="correctWord">' + one_word[0] + '</span>')
            else:            
                one_sent.append(' ' + '<span class="wrongWord">' + one_word[0] + '</span>')
                count += 1
    
        x = self.len_list[-1]*0.33
        if count > x:
            one_sent.insert(0, '<span class="Complex sentence">')
        else:
            one_sent.insert(0, '<span class="Simple sentence">')
        one_sent.append('</span>')
    
        self.visible_text.append(one_sent)
