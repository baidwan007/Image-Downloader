import requests 
from bs4 import BeautifulSoup
import cssutils #package to parse css 
import sys
from urllib.parse import urljoin # for making proper path addresses depending on absolute and relative paths
import logging #to turn off the useless warning and error printing of cssutils

cssutils.log.setLevel(logging.CRITICAL) #to turn off the useless warning and error printing of cssutils

"""this function creates the final css object by taking css string input from cssCreator function. it returns that css object"""
def parser(url):
  return_list = cssCreator(url)
  ext_int_css_object = cssutils.parseString(return_list[0])
  inline_css_object=cssutils.parseStyle(return_list[1])
  import_css_object=import_checker(ext_int_css_object,return_list[2])
  #print (ext_int_css_object) #<cssutils.css.CSSStyleSheet object encoding='utf-8' href=None media=None title=None namespaces={} at 0x7f971a22fbe0>
  #print (inline_css_object) #<cssutils.css.CSSStyleDeclaration object length=2 (all: 3) at 0x7f971a22f0b8>
  #print (import_css_object) #<cssutils.css.CSSStyleSheet object encoding='utf-8' href=None media=None title=None namespaces={} at 0x7f26d405c400>
  return [ext_int_css_object, inline_css_object, import_css_object]

"""this function creates the entire css string by calling separate functions for external, internal and inline stylesheets. it returns those strings"""
def cssCreator(url):
  r=requests.get(url)
  soup=BeautifulSoup(r.text)
  ext_css_list = extCssCreator(soup , url)
  import_url_helper= ext_css_list[1]
  ext_css_string = ext_css_list[0]
  int_css_string = intCssCreator(soup)
  inline_css_string = inlineCssCreator(soup)
  ext_int_css_string = ext_css_string + int_css_string 
  return [ext_int_css_string, inline_css_string, import_url_helper]
  
"""This function parses the html of the webpage and finds the links of external stylesheets. it then hits those urls and gets the css present in them as a string. it appends these css strings from all the external stylesheet urls it hit hence having one string with the entire css of all the external stylesheets. this function returns al list in which list[0] is this css string and the 2nd argument is one of the url links of the stylesheet. this is returned in order to let the importCssCreator function to create the absolute url in case import command is used in the stylesheet"""
def extCssCreator(soup , url):
  fetched = soup.head.findAll('link',{'rel':'stylesheet'})
  fetched_url=[]
  for i in fetched:
    fetched_url.append(i['href'])
  final_url=[]
  print (len(fetched_url))
  ext_css_string=" "
  if len(fetched_url)==0:
    return [ext_css_string," "]
  else:
    for i in fetched_url:
      final_url.append(urljoin(url,i)) #creating absolute urls
    for i in final_url:
      print (i)
      r=requests.get(i) #hitting those urls to get the data
      ext_soup = BeautifulSoup(r.text)
      try:
        if ext_soup.head.title == '404 Not Found':#in case the url is wrong
          print ("404 error")
          continue
      except AttributeError:
        pass
      ext_css_string=ext_css_string+ext_soup.p.text  #creating a string of the css
    try:
      list1=[ext_css_string,final_url[0]]
    except IndexError:
      return [lst1[0],"/"]
    else:
      return list1


"""this finds any internal stylesheet that may be present. if yes creates a string of it and returns it"""
def intCssCreator(soup):
  style_tag_list=soup.findAll('style',{'type':'text/css'})
  int_css_string=''
  for i in style_tag_list:
    int_css_string=int_css_string+i.text
  return int_css_string

"""this finds any inline stylesheet that may be present. if yes creates a string of it and returns it"""
def inlineCssCreator(soup):
  style_tag_list=soup.body.findAll(attrs={'style': True})
  inline_css_string=" "
  for i in style_tag_list:
    print (i['style'])
    inline_css_string=inline_css_string+";"+i['style']
  return inline_css_string

"""the external stylesheets may have import urls at times. Those urls must be hit and css extracted from them. This function does this"""
def import_checker(ext_int_css_object,url):
  initial_url_list=[]
  final_url_list=[]
  import_css_string=""
  # generating a list of urls present in import tag if any at all
  for i in ext_int_css_object.cssRules:
    try:
      initial_url_list.append([i.href])
    except AttributeError:
      pass
  for i in initial_url_list:
    print (i)
  if len(initial_url_list)!=0:
    for i in initial_url_list:
      final_url_list.append(urljoin(url,i[0]))
    #hitting each url 
    for i in final_url_list:
      print (i)
      r=requests.get(i)
      soup = BeautifulSoup(r.text)
      try:
        if soup.head.title == '404 Not Found':
          print ("404 error")
          continue
      except AttributeError:
        pass
      #extracting css from each url that has been hit
      import_css_string=import_css_string+soup.p.text
  if len(import_css_string)!=0:
    import_css_object=cssutils.parseString(import_css_string)
    return import_css_object
  else:
    return 0
  
#object1=parser('https://www.hipmunk.com/')
#object1=parser('http://paceoil.ca/') this page's stylesheet has import tags.. so helps in checking the working of import_checker function
if __name__=='__main__':
  try:
    object1= parser(sys.argv[1])
    print (object1)
  except IndexError:
    print ('\n')
    print ('*'*25,'Hello!!','*'*25)
    print ('\n')
    print ('This script takes the url of a page as the only command line argument, it parses the entire css of the page -> hence converting it into an object for our fiddeling and the def parser returns this css object as a list with three elements. list[0] is the external_stylesheet_css_object. list[1] is the inline_css object. list[2] has the css object created if there is import statement in external stylesheet. if not then list[2] is set to 0')
    print ('pass the url of the page from the command line after the script name eg pthon3 css_extractor.py https://www.hipmunk.com/')
    print ('\n')



  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    