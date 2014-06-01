#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import urllib
from urllib import urlopen
from lexchecker import LexChecker
import os, cgi
#from vvodchecker import VvodChecker

LIB64_DIR = '/home/k/karpnv/lib64/python2.7/site-packages'
sys.path.insert(0, LIB64_DIR)
import nltk
import pymorphy2
#from pymorphy import get_morph
import urllib

CONTENT_HEADER = 'Content-Type: text/html; charset=utf-8'
PAGE_HEAD = u"""
<!DOCTYPE HTML>
<html>
 <head>
  <meta charset="utf-8">
  <title>Адаптация текста</title>
<link type="text/css" rel="stylesheet" href="stylesheet.css"/>
 </head>
 <body>
 <p>
 Выберите целевой уровень владения языком </br>
 <form action="textarea.py" method="post">
<input type="radio" name="group2" value="a1"> <span class="case">Элементарный</span>  </br>
<input type="radio" name="group2" value="a2"> <span class="case">Базовый</span></br>
<input type="radio" name="group2" value="b1" checked> <span class="case">Первый сертифицируемый</span>  </br>
</p>
<table > 
<tr> <td><b>Введите ваш текст для обработки:</b>
</td> <td>
</td><td><b>Результат обработки:</b>
</td><td></td></tr>
<tr> 
<td>  
    <p><textarea rows="20" cols="55" name="text" >%s</textarea></p>
</td> 
<td> 
    <p><input type="submit" value="> Обработать >"></p>
</td> 
<td class='result'> 
    <div  class="divsprocr">"""

PAGE_FOOT = u"""
</div>

</td> <td></td>
</tr>
</table>
  
<table>
<tr> 
<td> Поиск в тексте </td>
<td> <input type="radio" name="group1" value="a" checked> <span class="wrongWord">пассивной лексики</span> или </td> 
<td> <input type="radio" name="group1" value="b"> <span class="wrongWord">сложных конструкций</span> </td>
</tr> 

</table>
    </form>
 </body>
</html>"""

def process(text, lexchecker):
    out=''
    #LexicalMinimum = urllib.urlopen('http://lingvocourse.ru/www/public_html/cgi-bin/simp/Data/lexmin.txt').read().decode('utf-8')
    #text = urllib.urlopen('http://lingvocourse.ru/www/public_html/cgi-bin/simp/Data/corpus.txt').read().decode('utf-8')

    ##For loading data from file please uncomment and edit following strings
    ##import csv
    ##text = csv.reader(open('Data/file.csv', 'rb'), delimiter='', quotechar = '')
    lexchecker.cut_sentence(text)
    for element in lexchecker.visible_text:
        for e in element:
            out=out+e.encode('utf-8')
    return out

def print_text(request,resp):
    print CONTENT_HEADER
    print (PAGE_HEAD  % (request)).encode('utf-8')
    print resp
    print (PAGE_FOOT).encode('utf-8')    
    return

def print_error(str):
    print CONTENT_HEADER
    print (PAGE_HEAD  % ('')).encode('utf-8')
    print str
    print (PAGE_FOOT).encode('utf-8') 
    return

def main():
    f = cgi.FieldStorage()
    #print_text('dddd')
    if f.has_key("text"):
        text=f["text"].value
        text = unicode(text, 'utf-8')
        lexchecker = LexChecker(f["group2"].value)#f["group2"].value
        if text!='' and f["group1"].value=="a":
            resp=process(text,lexchecker)
            print_text(text,resp)
        elif text!='' and f["group1"].value=="b":
            resp=lexchecker.check_vvod_words(text)
            resp=lexchecker.findCompStruct(resp.encode('utf-8'))
            print_text(text,resp)
        elif text!='' and f["group1"].value=="c":
            resp=lexchecker.findCompStruct(text.encode('utf-8'))
            print_text(text,resp)
        else:
            print_error("No data to process")
    else:
        print_error("No data to process")
      
if __name__ == '__main__':
    main()