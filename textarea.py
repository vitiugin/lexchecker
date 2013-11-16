#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os, cgi
import urllib
from urllib import urlopen
from lexchecker import LexChecker


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
<table > 
<tr> <td><b>Введите ваш текст для обработки:</b>
</td> <td>
</td><td><b>Результат обработки:</b>
</td></tr>
<tr> 
<td>  <form action="textarea.py" method="post">
    <p><textarea rows="15" cols="45" name="text" >%s</textarea></p>
</td> 
<td> 
    <p><input type="submit" value="> Обработать >"></p>
</td> 
<td class='result'> 
    <div  class="divsprocr">"""

PAGE_FOOT = u"""
</div>

</td> 
</tr> </table>
    </form>
 </body>
</html>"""

def process(text):
    lexchecker = LexChecker()
    LexicalMinimum = urllib.urlopen('http://lingvocourse.ru/www/public_html/cgi-bin/simp/Data/lexmin.txt').read().decode('utf-8')
    #text = urllib.urlopen('http://lingvocourse.ru/www/public_html/cgi-bin/simp/Data/corpus.txt').read().decode('utf-8')

    ##For loading data from file please uncomment and edit following strings
    ##import csv
    ##text = csv.reader(open('Data/file.csv', 'rb'), delimiter='', quotechar = '')
    lexchecker.cut_sentence(text)
    for element in lexchecker.visible_text:
        for e in element:
            print e.encode('utf-8')
    return 

def print_text(request):
    request = unicode(request, 'utf-8')
    response=request
    print CONTENT_HEADER
    print (PAGE_HEAD  % (request)).encode('utf-8')
    process(request)
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
        if text!='':
            print_text(text)
        else:
            print_error("No data to process")
    else: 
        print_error("No data to process")
      
if __name__ == '__main__':
    main()