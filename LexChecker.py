#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys,re
LIB64_DIR = '/home/k/karpnv/lib64/python2.7/site-packages'
sys.path.insert(0, LIB64_DIR)

import pymorphy2
import nltk
import urllib


class LexChecker(object): 
    wordTagStart='<span class="%s">'
    sentenceTagStart ='<span class="%s">'
    tagStop='</span>'
    wordCount=0
    sentenceCount=0
    syllableCount=0
    letterNumberCount=0
    complexCount=0
    
    def __init__(self,level='a1'):
        self.morph = pymorphy2.MorphAnalyzer()
        self.final_sentence = []
        self.len_list = []
        self.visible_text = []
        self.lexical_minimum = urllib.urlopen('https://raw.github.com/fedorvityugin/lexchecker/master/Data/lexmin_elementary.txt').read().decode('utf-8')
        if level=='a2':
            self.lexical_minimum = self.lexical_minimum + urllib.urlopen('https://raw.github.com/fedorvityugin/lexchecker/master/Data/lexmin_basic.txt').read().decode('utf-8')
        if level=='b1':
            self.lexical_minimum = self.lexical_minimum + urllib.urlopen('https://raw.github.com/fedorvityugin/lexchecker/master/Data/lexmin_basic.txt').read().decode('utf-8')
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
        return self.visible_text
    
    
    def check_vvod_words(self,sentence):
        sentence=sentence
        fpg = urllib.urlopen( 'https://raw.github.com/fedorvityugin/lexchecker/master/Data/vvodn.txt').read().decode('utf-8')
        for line in fpg.split('\n'):
            #line = line.encode('utf8')
            line = line.strip()
            template_1 = line + ','
            template_2 = ', '+ template_1
            res = sentence
            index_1 = sentence.lower().find(template_1)
            index_2 = sentence.lower().find(template_2)
            flgEdited = 0
            if(index_2 != -1):
                res= sentence[:index_2]+'<span class="wrongWord">'+sentence[index_2:index_2+len(template_2)]+'</span>'+sentence[index_2+ len(template_2):]
                flgEdited = 1
                if(index_1 != -1):
                    tmp = res.strip()
                    index_1 = res.strip().find(template_1)
                    res = tmp[:index_1] + '<span class="wrongWord">'+tmp[index_1:index_1+len(template_1)]+'</span>'+tmp[index_1+ len(template_1):]
                    break
            if(index_1 != -1):
                res= sentence[:index_1]+'<span class="wrongWord">'+sentence[index_1:index_1+len(template_1)]+'</span>'+sentence[index_1+ len(template_1):]
                break

        res=res
        return res.strip()
        
    def findCompStruct(self,sentence):
        sentence=sentence
        regexpList = [r", ?(коль|коли|кабы|ежели|дабы|ибо|(даром что)|нежели).*", 
        r", ?правда ?,", r"^П|правда,.*",r"(там|туда|оттуда|везде|всюду|оттуда), (где|куда|откуда).*",
        r"как|(подобно тому как)|(ровно тому как).*",
        r", ?как .*", r"(подобно тому)|(ровно тому), ?как .*", r"((как будто)|будто|словно|точно).*,.*",
        r", ?((как будто)|будто|словно|точно) .*", r"^Е|если .*, ?то .*", r"^М|между тем как .*", r", ?между тем как .*", r"^Р|ровно как .*,.*", 
        r", ?ровно как .*", r"^Т|так же как .*,.*", r", ?так же как .*", r"^П|поскольку .*, ?постольку .*", r"поскольку, ?постольку .*", 
        r", ?(и|а|но|да|тоже|также|ни|зато|однако|(то ли)|или|только|(не то)|(да и)|(но и)) и .*, ?(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|(будто бы)|как|словно|ли|кто|что|который|какой|чтобы|(как будто)|будто|словно|насколько|пока|(пока не)|как|(как только)|(лишь только)|(едва только)|(стоило как)|(не прошло как)|если|(если бы)|когда|кабы|(как раз)|скоро|ежели|(если бы)|(когда бы)|коли|коль|(для того чтобы)|(с той целью чтобы)|дабы|(только бы)|(лишь бы)|(потому что)|(оттого что)|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(в виду того что)|(тем более что)|хотя|хоть|пусть|пускай|(даром что)|(несмотря на то, ?что)|(невзирая на то, ?что)|(, ?правда,)|(так что)|чем|нежели) .*", 
        r", ?(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|(будто бы)|как|словно|ли|кто|что|который|какой|чтобы|(как будто)|будто|словно|насколько|пока|(пока не)|как|(как только)|(лишь только)|(едва только)|(стоило как)|(не прошло как)|если|(если бы)|когда|кабы|(как раз)|скоро|ежели|(если бы)|(когда бы)|коли|коль|(для того чтобы)|(с той целью чтобы)|дабы|(только бы)|(лишь бы)|(потому что)|(оттого что)|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(в виду того что)|(тем более что)|хотя|хоть|пусть|пускай|(даром что)|(несмотря на то, ?что)|(невзирая на то, ?что)|(, ?правда,)|(так что)|чем|нежели) .*, ?(и|а|но|да|тоже|ни|также|зато|однако|(то ли)|или|только|(не то)|(да и)|(но и)) .*",
        r", ?(и|а|но|да|тоже|также|ни|зато|однако|(то ли)|или|только|(не то)|(да и)|(но и)) .*:.*", 
        r": ?.*,?(и|а|но|да|тоже|также|ни|зато|однако|(то ли)|или|только|(не то)|(да и)|(но и)) .*", 
        r", ?(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|(будто бы)|как|словно|ли|кто|что|который|какой|чтобы|(как будто)|будто|словно|насколько|пока|(пока не)|как|(как только)|(лишь только)|(едва только)|(стоило как)|(не прошло как)|если|(если бы)|когда|кабы|(как раз)|скоро|ежели|(если бы)|(когда бы)|коли|коль|(для того чтобы)|(с той целью чтобы)|дабы|(только бы)|(лишь бы)|(потому что)|(оттого что)|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(в виду того что)|(тем более что)|хотя|хоть|пусть|пускай|(даром что)|(несмотря на то, ?что)|(невзирая на то, ?что)|(, ?правда,)|(так что)|чем|нежели) .*:.*", 
        r".*:.*, (который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|(будто бы)|как|словно|ли|кто|что|который|какой|чтобы|(как будто)|будто|словно|насколько|пока|(пока не)|как|(как только)|(лишь только)|(едва только)|(стоило как)|(не прошло как)|если|(если бы)|когда|кабы|(как раз)|скоро|ежели|(если бы)|(когда бы)|коли|коль|(для того чтобы)|(с той целью чтобы)|дабы|(только бы)|(лишь бы)|(потому что)|(оттого что)|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(в виду того что)|(тем более что)|хотя|хоть|пусть|пускай|(даром что)|(несмотря на то, ?что)|(невзирая на то, ?что)|(, ?правда,)|(так что)|чем|нежели) .*", 
        r", ?(и|а|но|да|тоже|также|ни|зато|однако|(то ли)|или|только|(не то)|(да и)|(но и)) .*, ?(который|чей|что|какой|где|куда|откуда|когда|что|чтобы|будто|(будто бы)|как|словно|ли|кто|что|который|какой|чтобы|(как будто)|будто|словно|насколько|пока|(пока не)|как|(как только)|(лишь только)|(едва только)|(стоило как)|(не прошло как)|если|(если бы)|когда|кабы|(как раз)|скоро|ежели|(если бы)|(когда бы)|коли|коль|(для того чтобы)|(с той целью чтобы)|дабы|(только бы)|(лишь бы)|(потому что)|(оттого что)|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(так как)|(из-за того что)|ибо|(благодаря тому что)|(в виду того что)|(тем более что)|хотя|хоть|пусть|пускай|(даром что)|(несмотря на то, ?что)|(невзирая на то, ?что)|(, ?правда,)|(так что)|чем|нежели) .*:.*",
        r"((Т|т)олько)",r"((Л|л)ишь)",r"((П|п)очти)",r"((И|и)сключительно)",r"((В|в)се-таки)", r"((В|в)сё-таки)",r"((Ч|ч)то за)",r"((Д|д)аже)",r"(же)",r"((В|в)едь)"]
        
        for regexp in regexpList:
            pattern = re.compile(regexp, re.IGNORECASE)
            match =  pattern.search(sentence)
            if(match):
                start = match.span()[0]
                end = match.span()[1]
                sentence = sentence[0:start] + r'<span class="wrongWord">' + sentence[start:end]+ r'</span>'+sentence[end:len(sentence)]
                #sentence = sentence[0:start] + r'<span class="wrongWord">' + sentence[start:len(sentence)] + r'</span>'
        return sentence

