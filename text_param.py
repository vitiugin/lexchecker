# -*- coding: utf-8 -*-

import codecs
import re, csv

import nltk
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
final_list = []
poses = []
sum_sen_length = []
all_words = []
all_words_in_text = [] #список всех слов в тексте
sent_words_in_vowels = []
all_words_in_vowels = []

"""
----- Creating list of lexical minimum -----
"""

def open_lex_min_list(lex_min_list_file_name):
    lexical_minimum = []

    fp = open(lex_min_list_file_name, 'r')
    line = fp.readline().encode('utf-8')
    while line:
        word = line.strip()
        lexical_minimum.append(word)
        line = fp.readline().encode('utf-8')
    fp.close()
    return lexical_minimum

def cut_text(full_text):
    list_of_sentences = nltk.PunktSentenceTokenizer().tokenize(full_text)
    sen_num = float(len(list_of_sentences))
    for s in list_of_sentences:
        cut_sentence(s)

    sum = 0.0
    for word in all_words:
        sum += len(word) #сумма букв в предложении
        all_words_in_text.append(word)
        lemmatise(word)

    sym_count = 0
    word5 = 0
    word6 = 0
    word7 = 0
    word8 = 0
    word9 = 0
    word10 = 0
    word11 = 0
    word12 = 0
    word13 = 0
    for w in all_words_in_text:
        sym_count += len(w)
        if len(w) > 4:
            word5 += 1
        if len(w) > 5:
            word6 += 1
        if len(w) > 6:
            word7 += 1
        if len(w) > 7:
            word8 += 1
        if len(w) > 8:
            word9 += 1
        if len(w) > 9:
            word10 += 1
        if len(w) > 10:
            word11 += 1
        if len(w) > 11:
            word12 += 1
        if len(w) > 12:
            word13 += 1

    final_list.append(sym_count/sen_num)
    final_list.append(sym_count/float(len(all_words_in_text)))
    final_list.append(word5/float(len(all_words_in_text)))
    final_list.append(word6/float(len(all_words_in_text)))
    final_list.append(word7/float(len(all_words_in_text)))
    final_list.append(word8/float(len(all_words_in_text)))
    final_list.append(word9/float(len(all_words_in_text)))
    final_list.append(word10/float(len(all_words_in_text)))
    final_list.append(word11/float(len(all_words_in_text)))
    final_list.append(word12/float(len(all_words_in_text)))
    final_list.append(word13/float(len(all_words_in_text)))
    del all_words_in_text[:]

    count = 0
    for vow_num in sent_words_in_vowels:
        count += vow_num
    final_list.append(count/sen_num)
    del sent_words_in_vowels[:]

    summ = 0
    for number in sum_sen_length:
        summ += number

    w = 0
    vow3 = 0
    vow4 = 0
    vow5 = 0
    vow6 = 0
    for vow in all_words_in_vowels:
        w += vow
        if vow > 2:
            vow3 +=1
        if vow > 3:
            vow4 +=1
        if vow > 4:
            vow5 +=1
        if vow > 5:
            vow6 +=1

    words_in_sent = float(len(all_words))
    final_list.append(w/sum)
    final_list.append(vow3/words_in_sent)
    final_list.append(vow4/words_in_sent)
    final_list.append(vow5/words_in_sent)
    final_list.append(vow6/words_in_sent)

    av_sen_length = summ / sen_num
    final_list.append(av_sen_length)
    av_word = sum / len(all_words)
    final_list.append(av_word)
    final_list.append(sum)
    final_list.append(len(all_words))

    finding(poses)
    # [av vowels in sent, av vowels in text, % of word5, % of word6, % of word7, % of word8, % of word9, % of word10, % of word11, % of word12, % of word13, % of vow3, % of vow4, % of vow5, % of vow6, av len of words in sent, av len of words in symbols, av # words in sent, av word len in words, text in symbols, text_in words, pos, pos, ..., pos]
    # тут типа все параметры кроме проверки на лексический минимум
    print final_list
    del final_list[:], sum_sen_length[:], all_words[:], poses[:], all_words_in_vowels[:]

def cut_sentence(sentence):
    list_of_words = re.split(r'[\s+\t\n\.\|\:\–\/\,\?\!\"()]+', sentence)
    sen_length = float(len(list_of_words[:-1]))
    sum_sen_length.append(sen_length)
    for w in list_of_words:
        all_words.append(w)
    return



def lemmatise(word):
    list_of_vowels = [u'а', u'у', u'о', u'ы', u'и', u'э', u'я', u'ю', u'ё', u'е']
    word = word.lower()
    count = 0
    for symbol in word:
        if symbol in list_of_vowels:
            count += 1
    #print count
    sent_words_in_vowels.append(count)
    all_words_in_vowels.append(count)

    try:
        word_in_work = morph.parse(word)[0]
        poses.append(word_in_work.tag.POS)
    except IndexError:
        return

def finding(list_of_pos): #смторим, какие части речи есть в текстх, только наличие
    if u'NOUN' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'ADJF' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'ADJS' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'COMP' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'VERB' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'INFN' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'PRTF' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'PRTS' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'GRND' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'NUMR' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'ADVB' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'NPRO' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'PRED' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'PREP' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'CONJ' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'PRCL' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)
    if u'INTJ' in list_of_pos:
        final_list.append(1)
    else:
        final_list.append(0)

# ----- Data -----

lexmin = codecs.open('lexmin.txt', 'r', 'utf-8') #ссылка на файл с лексическим словарем - lexmin0.txt, lexmin1.txt, lexmin2.txt - словари по уровням elementary, basic, first
lexical_minimum = lexmin.read()

# здесь подрубаем тексты, которые хотим проанализировать
#m = 1
#while m < 51:
#    n = 'news/' + str(m) + '.txt'
#    text_file = codecs.open(n, 'r', 'utf-8')
#    text = text_file.read()
#    cut_text(text)
#    m += 1

with codecs.open('fb-posts.txt', 'r', 'utf-8') as f:
    content = f.readlines()
    for text in content:
        cut_text(text)