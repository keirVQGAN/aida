import cv2
from glob import glob
import shutil
import os
import os.path
from google.colab import drive
from dirsync import sync
from rich.console import Console
console = Console()
from slugify import slugify
import configparser
import IPython
import tarfile
import shutil
from IPython.display import Image
import time
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd


def sumUrl(urlIn,sentences):
    from sumy.parsers.html import HtmlParser
    from sumy.nlp.tokenizers import Tokenizer
    LANGUAGE = "english"
    url = urlIn
    parser = HtmlParser.from_url(urlIn, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer(parser.document, sentences):
        print(sentence)
    
def sumTxt(txtIn,sentences):
    from sumy.parsers.html import HtmlParser
    from sumy.nlp.tokenizers import Tokenizer
    LANGUAGE = "english"
    with open(txtIn, 'r') as file:
        txt = file.read()
    stemmer = Stemmer(LANGUAGE)
    parser = PlaintextParser.from_string((txt), sumytoken(LANGUAGE))
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer(parser.document, sentences):
        print(sentence)

def soupURL(req):
  pdTemp = {req: []}
  html_page = urlopen(req)
  soupUrlPd = pd.DataFrame(data=pdTemp)
  soup = BeautifulSoup(html_page, "lxml")
  links = []
  for link in soup.findAll('a'):
      links.append(link.get('href'))
  links = [x for x in links if x.startswith('https')]
  links = [x for x in links if not x.startswith('https://twitter')]
  links = [x for x in links if not x.startswith('https://www.twitter')]
  links = [x for x in links if not x.startswith('https://insta')]
  links = [x for x in links if not x.startswith('https://www.insta')]
  links = [x for x in links if not x.startswith('https://google')]
  links = [x for x in links if not x.startswith('https://www.google')]
#   df = pd.DataFrame(links, columns=[req])
#   dc = df.drop_duplicates()
  return links
  
def urlName(url):
  head, tail = os.path.split(url)
  return(tail)

#Functions
##Map config section to dictionary

def confRead(file='content/config_aida.ini'):
  import configparser
  config_file = file
  config = configparser.configParser()
  config.read(config_file)

def confDict(section):
  dict1 = {}
  options = config.options(section)
  for option in options:
      try:
          dict1[option] = config.get(section, option)
          if dict1[option] == -1:
              DebugPrint("skip: %s" % option)
              
      except:
          print("exception on %s!" % option)
          dict1[option] = None
  return dict1
##Print config (section) to console

def confPrint(section):
  confDict = confDict(section)
  confPrint = "\n".join("{}\t{}".format(k, v) for k, v in confDict.items())
  print(f'[{section}]')
  print(confPrint)


def clone():
  sample_data=os.path.isdir("/content/sample_data")
  drive.mount('/mnt/drive')
  sync('/mnt/drive/MyDrive/aida/in', '/content/in', 'sync', create=True)
  os.makedirs('/content/out/', exist_ok="True")
  if sample_data==1:
    shutil.rmtree('/content/sample_data')

def txtH(action):
    console.print(f"[bright_white]{action}[/bright_white]")

def txtL(action):
    console.print(f"[r black]{action}[/r black]")

def txt(action, details):
    console.print(f"[bright_white]{action}[/bright_white] -> [r black]{details}[/r black]")

def txtM(action, details):
    console.print(f"[bright_magenta]{action}[/bright_magenta] -> [r black]{details}[/r black]")

def txtC(action, details):
    console.print(f"[bright_cyan]{action}[/bright_cyan] -> [r black]{details}[/r black]")

def txtY(action, details):
    console.print(f"[bright_yellow]{action}[/bright_yellow] -> [r black]{details}[/r black]")

def txtB(action, details):
    console.print(f"[bright_black]{action}[/bright_black] -> [r black]{details}[/r black]")

def mount():
    drive.mount('/mnt/drive')

def syncDir(source, target):  
    sync(source, target, 'sync', create=True)

def rm(dir):
    shutil.rmtree(dir)
    
def cp(filename,target):
    shutil.copyfile(file,dest)   

def gifShow(Path):
  with open(Path,'rb') as f:
      a = display.Image(data=f.read(), format='png')
      return a

def mk(dir):
    os.makedirs(dir, exist_ok="True")
    
def lsDir(dir):
    return [os.path.join(dir, file) for file in os.listdir(dir)]

def time():
    return [time.strftime("_%H%M%S")]

def zip(filename, source):
    with tarfile.open(filename, "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))

def uzip(filename, target):
    my_tar = tarfile.open(filename)
    my_tar.extract(target)
    my_tar.close()
    
def ls(dir):
    return [os.path.join(dir, file) for file in os.listdir(dir)]

def ls2str(ls):
    return " ".join(ls)

def name(file_path):
  basename = os.path.basename(file_path)
  file_name = os.path.splitext(basename)[0]
  return file_name
