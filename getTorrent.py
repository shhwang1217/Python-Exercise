#!/usr/bin/env python

import sys
import urllib.request
import re
import time
from html.parser import HTMLParser

class MyHtmlParse(HTMLParser):
  def __init__(self, regExp ):
    HTMLParser.__init__(self)
    self.__href = ""
    self.__title = ""
    self.__wantData = False
    self.__regExp = regExp
    self.hrefList = []
    
  def handle_starttag(self, tag, attrs):
    if tag == "a" :
      for attr in attrs :
        if attr[0] == "href" :
          m = re.match( self.__regExp, attr[1] )  # e.g __regExp = ".*\.torrent$"
          if m :
            self.__href = attr[1]            
            self.__wantData = True
            break
          
  def handle_data(self, data):
    if self.__wantData :
      self.__title = data
  
  def handle_endtag(self, tag):
    if self.__wantData :  
      self.hrefList.append( [ self.__href, self.__title ] )  
      self.__href = ""
      self.__title = ""
      self.__wantData = False


def findAllHrefs( url, regEx ):
  response = urllib.request.urlopen( url )
  html = response.read()
  parser = MyHtmlParse( regEx )
  parser.feed( html.decode() )
  return parser.hrefList

  
#sys.exit("Exit")

# main
#param_start= sys.argv[1] 
#param_end= sys.argv[2] 

# The URL contains all hrefs we wants

param_total_url = "https://share.dmhy.org/topics/list?keyword=%5B%E9%8A%80%E8%89%B2%E5%AD%90%E5%BD%88%E5%AD%97%E5%B9%95%E7%B5%84%5D%5B%E5%90%8D%E5%81%B5%E6%8E%A2%E6%9F%AF%E5%8D%97%5D+%5B%E7%B9%81%E6%97%A5%E9%9B%99%E8%AA%9EMP4%5D%5B720P%5D&sort_id=0&team_id=576&order=date-desc"

param_page_regEx = ".*/topics/view/.*\.html$"
param_torrent_regEx = ".*\.torrent$"

pages = findAllHrefs( param_total_url, param_page_regEx )

i = 0
for p in pages :
  url = "https://share.dmhy.org" + p[0]
  # 濾出範圍內的才需要處理
  # print( "URL = {}".format( url ) )
  if i >= 58 :
    break
  i = i + 1
  torrent = findAllHrefs( url, param_torrent_regEx )
  if len(torrent) == 1 :
    href = torrent[0][0]
    fname = torrent[0][1]
    print( "Save {} to {}".format( href, fname ) )
    urllib.request.urlretrieve( "https:" + href, fname + ".torrent" )
    
    