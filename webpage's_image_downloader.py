import sys,os
import re
import requests
import bs4
from bs4 import BeautifulSoup
import css_extractor # a script written by me present in the same directory
from css_extractor import parser
from urllib.parse import urljoin
import urllib


"""this takes the url of the site as the argument.. gets the url list of all the images of that site by calling htmlImgSearch and cssImgSearch functions.. and then hits each of those urls to download the image on our system"""
def ImgDownloader(url):
  html_img_url_list=htmlImgSearch(url)
  css_img_url_list=cssImgSearch(url)
  parent_folder_name="downloaded_data_of_webpages/"+url.split('/')[2]
  os.mkdir(parent_folder_name)
  html_folder=parent_folder_name+"/imagesFromHtml"
  css_folder=parent_folder_name+"/imagesFromCss"
  os.mkdir(html_folder)
  os.mkdir(css_folder)
  for i in html_img_url_list:
    image_name=html_folder+'/'+i.split('/')[-1]
    try:
      urllib.request.urlretrieve(i,image_name)
    except:
      print ("image at ", i, "could not be downloaded")
  for i in css_img_url_list:
    image_name=css_folder+'/'+i.split('/')[-1]
    try:
      urllib.request.urlretrieve(i,image_name)
    except:
      print ("image at ", i, "could not be downloaded")
  return


"""takes the url of the site as input. returns the url list containing urls of all the images present in the html"""
def htmlImgSearch(url):
  print ("inside html")
  r=requests.get(url)
  soup=BeautifulSoup(r.text)
  tag_list=soup.findAll('img')
  url_list=[]
  final_url_list=[]
  for i in tag_list:
    try:
      url_list.append(i['src'])
    except KeyError:
      pass
  for i in url_list:
    final_url_list.append(urljoin(url,i))
  for i in final_url_list:
    print (i)
  return final_url_list

"""takes the url of the site as input. returns the url list containing urls of all the images present in the css.. the parsed css is available from the css_extractor script that has been imported in this script"""
def cssImgSearch(url):
  css_list=parser(url)
  ext_css=css_list[0]
  inline_css=css_list[1]
  import_css=css_list[2]
  url_list=[]
  final_url_list=[]
  r=requests.get(url)
  soup=BeautifulSoup(r.text)
  try:
    fetched = soup.head.findAll('link',{'rel':'stylesheet'})
    css_url=urljoin(url,fetched[0]['href'])
  except IndexError:
    css_url=urljoin(url," ")
  pattern= 'url.*?\)'
  #fetching urls from external css 
  for i in ext_css.cssRules:
    try:
      string=i.style.getPropertyValue('background')
      l=re.search(pattern,string)
      url_list.append(l.group()[4:-1])
    except AttributeError:
      pass
  for i in ext_css.cssRules:
    try:
      string=i.style.getPropertyValue('background-image')
      l=re.search(pattern,string)
      url_list.append(l.group()[4:-1])
    except AttributeError:
      pass
  for i in ext_css.cssRules:
    try:
      string=i.style.getPropertyValue('content')
      l=re.search(pattern,string)
      url_list.append(l.group()[4:-1])
    except AttributeError:
      pass
    
  #fetching urls from the import tag if present in external css
  if import_css !=0:
    for i in import_css.cssRules:
      try:
        string=i.style.getPropertyValue('background')
        l=re.search(pattern,string)
        url_list.append(l.group()[4:-1])
      except AttributeError:
        pass
    for i in import_css.cssRules:
      try:
        string=i.style.getPropertyValue('background-image')
        l=re.search(pattern,string)
        url_list.append(l.group()[4:-1])
      except AttributeError:
        pass
    for i in import_css.cssRules:
      try:
        string=i.style.getPropertyValue('content')
        l=re.search(pattern,string)
        url_list.append(l.group()[4:-1])
      except AttributeError:
        pass 
      
  #fetching urls from inline css
  for  i in inline_css.children():
    print ("in inline css")
    #print(i)
    try:
      string=i.value
      l=re.search(pattern,string)
      url_list.append(l.group()[4:-1])
    except AttributeError:
      pass
    
  #creating a final list of all the urls fetched from the css       
  for i in url_list:
    try:
      final_url_list.append(urljoin(css_url,i))
    except SyntaxError:
      pass
  for i in final_url_list:
    print (i)
  return final_url_list


#ImgDownloader('https://www.hipmunk.com/') #link with many images in css
#ImgDownloader('https://pixabay.com/') #link with many images in html
#ImgDownloader('http://paceoil.ca/') #link with import command in external stylesheet

try:#running the script
  url=sys.argv[1]
except AttributeError:
  print ("*"*30,"hello","*"*30)
  print ("1.this script takes the url of a webpage as a command line argument. It then downloads all the images present on the webpage in a folder which this script creates in the same working directory() in which this script is present")
  print ("2. note that this script imports module \"css_extractor.py\" inside it. So kindly keep this script and css_extractor.py script in the same directory so that the css_extractor.py module can be correctly imported in this script ")
  print ("3 you need to explicitly make a folder in the working directory in which script is present with the name downloaded_data_of_webpages. the folder in which images of a particular webpage will be saved will be created by the script inside this folder. if this folder is not created by us then the script wont be able to find the specified path and would throw an error")
  print ("4. some images downloaded using this script may not get opened . while trying to open them they may show an error. this is not the scripts fault. It is the urls fault in the site.. that url may be such that it is of the form https://asfa/asf/asfd/afs.jpg but when you actually hit the url, nothing is present there.")

ImgDownloader (url)


