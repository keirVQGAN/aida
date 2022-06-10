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
import sys

def txtH(action):
    console.print(f"[bright_white]{action}[/bright_white]")

def txtL(action):
    console.print(f"[r black]{action}[/r black]")

def txt(action, details):
    console.print(f"[bright_white]{action}[/bright_white] [r black]{details}[/r black]")

def txtM(action, details):
    console.print(f"[bright_magenta]{action}[/bright_magenta] -> [r black]{details}[/r black]")

def txtC(action, details):
    console.print(f"[bright_cyan]{action}[/bright_cyan] -> [r black]{details}[/r black]")

def txtY(action, details):
    console.print(f"[bright_yellow]{action}[/bright_yellow] -> [r black]{details}[/r black]")

def txtB(action, details):
    console.print(f"[bright_black]{action}[/bright_black] -> [r black]{details}[/r black]")


#TIME TAKEN
def timeTaken(start_time):
  import time
  timeTakenFloat = "%s seconds" % (time.time() - start_time)
  timeTaken = timeTakenFloat
  timeTaken_str = str(timeTaken)
  timeTaken_split = timeTaken_str.split('.')
  timeTakenShort = timeTaken_split[0] + '' + timeTaken_split[1][:0]
  txtM('Rendered in:',f'{timeTakenShort} Seconds')

def _preProcess(_project,_init_image,_scenes,_quality):
  #SAVE SETTING TO CSV
  import csv
  sceneCSV='/mnt/drive/MyDrive/aida/out/scenes_master.csv'
  with open(sceneCSV, 'a') as csvFile:
      writer = csv.writer(csvFile)
      # writer.writerow(['when', 'scenes', 'image_file', 'quality']
      writer.writerow([_project,_scenes, _init_image, _quality])
  csvFile.close()
  df = pd.read_csv(sceneCSV)
  df_new = df.drop_duplicates()
  df_new.to_csv(sceneCSV, index=False)
  #-------------------------------------------------------------------------------
  #RESIZE INIT
  from PIL import Image
  from PIL import ImageFile
  ImageFile.LOAD_TRUNCATED_IMAGES = True
  RESIZED_IMAGE_FILE = '/content/in/init/init.tif'
  TARGET_SIZE = 2000
  image = Image.open(_init_image)
  width, height = image.size
  if width >= height:
      new_width = TARGET_SIZE
      new_height = (height * TARGET_SIZE) // width
  else:
      new_width = (width * TARGET_SIZE) // height
      new_height = TARGET_SIZE
  resized_image = image.resize((new_width, new_height), resample=Image.LANCZOS)
  resized_image.save(RESIZED_IMAGE_FILE)
  image = Image

def draft(_scenes,_project,_style):
  import imageio
  import csv
  _confLs=[]
  for _thresh in range(20, 231, 20):
    #make masks
    maskPath=f'/content/in/mask/{_project}'
    confPath=f'/content/out/txt2img/config/conf'
    img = cv2.imread('/content/in/init/init.tif')
    os.makedirs(maskPath, exist_ok="True")
    ret, img_binary = cv2.threshold(img, _thresh, 255, cv2.THRESH_BINARY)
    imageio.imwrite(f'{maskPath}/{_project}_mask{_thresh}.jpg',img_binary) 
    _thresh = str(_thresh)
    _yaml = f'{confPath}/{_project}_mask{_thresh}.yaml'
    f = open(_yaml, "a")
    f.write(f"""#@package _global_
    scenes: {_scenes}
    file_namespace: {_project}-{_scenes}_mask{_thresh}
    scene_suffix: :0.8_[/content/in/mask/{_project}/{_project}_mask{_thresh}.jpg]
    direct_image_prompts: {_style}:0.8
    steps_per_scene: 2500
    save_every: 500
    width: 200
    cutouts: 200
    cut_pow: 2.5
    pixel_size: 3
    gradient_accumulation_steps: 2""")
    _confLs.append(_yaml)
    f.close()
    
def test(_scenes,_project,_style):
  import imageio
  import csv
  _confLs=[]
  for _thresh in range(20, 231, 20):
    #make masks
    maskPath=f'/content/in/mask/{_project}'
    confPath=f'/content/out/txt2img/config/conf'
    img = cv2.imread('/content/in/init/init.tif')
    os.makedirs(maskPath, exist_ok="True")
    ret, img_binary = cv2.threshold(img, _thresh, 255, cv2.THRESH_BINARY)
    imageio.imwrite(f'{maskPath}/{_project}_mask{_thresh}.jpg',img_binary) 
    _thresh = str(_thresh)
    _yaml = f'{confPath}/{_project}_mask{_thresh}.yaml'
    f = open(_yaml, "a")
    f.write(f"""#@package _global_
    scenes: {_scenes}
    file_namespace: {_project}-{_scenes}_mask{_thresh}
    scene_suffix: :0.8_[/content/in/mask/{_project}/{_project}_mask{_thresh}.jpg]
    direct_image_prompts: {_style}:0.8
    steps_per_scene: 150
    save_every: 150
    width: 200
    cutouts: 20
    cut_pow: 2.5
    pixel_size: 3
    gradient_accumulation_steps: 1""")
    _confLs.append(_yaml)
    f.close()
    
def clone():
  sample_data=os.path.isdir('/content/sample_data')
  drive.mount('/mnt/drive')
  sync('/mnt/drive/MyDrive/aida/in', '/content/in', 'sync', create=True)
  os.makedirs('/content/out/', exist_ok="True")
  os.makedirs('/content/aida/txt2img', exist_ok="True")
  sync('/content/in/config', '/content/out/txt2img/config', 'sync', create=True)
  shutil.rmtree('/content/in/config')
  if sample_data==1:
    shutil.rmtree('/content/sample_data')

def sumUrl(urlIn,sentences):
    from sumy.parsers.html import HtmlParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers import luhn
    from sumy.utils import get_stop_words
    from sumy.nlp.stemmers import Stemmer
    from sumy.summarizers.luhn import LuhnSummarizer 
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer as sumytoken
    from sumy.summarizers.lex_rank import LexRankSummarizer
    from sumy.summarizers.lsa import LsaSummarizer as Summarizer
    from sumy.parsers.html import HtmlParser
    from sumy.nlp.tokenizers import Tokenizer
    LANGUAGE = "english"
    url = urlIn
    parser = HtmlParser.from_url(urlIn, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for sentence in summarizer(parser.document, sentences):
        return sentence
    
def sumTxt(txtIn,sentences):
    from sumy.parsers.html import HtmlParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers import luhn
    from sumy.utils import get_stop_words
    from sumy.nlp.stemmers import Stemmer
    from sumy.summarizers.luhn import LuhnSummarizer 
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer as sumytoken
    from sumy.summarizers.lex_rank import LexRankSummarizer
    from sumy.summarizers.lsa import LsaSummarizer as Summarizer
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
  pdTemp = []
  html_page = urlopen(req)
  soupUrlPd = pd.DataFrame(data=pdTemp)
  soup = BeautifulSoup(html_page, "lxml")
  links = []
  for link in soup.findAll('a', href=True):
      links.append(link.get('href'))
  filterList = ['https://you','https://medium','https://www.medium','https://creativecommons','https://face','https://www.face','https://twit','https://www.twit','https://inst','https://www.inst','https://go','https://www.goo']
  for filter in filterList:
    links = [x for x in links if not x.startswith(filter)]
    links = [x for x in links if x.startswith('https')]
#   links = [x for x in links if not x.startswith('https://www.facebook')]
#   links = [x for x in links if not x.startswith('https://twitter')]
#   links = [x for x in links if not x.startswith('https://www.twitter')]
#   links = [x for x in links if not x.startswith('https://insta')]
#   links = [x for x in links if not x.startswith('https://www.insta')]
#   links = [x for x in links if not x.startswith('https://google')]
#   links = [x for x in links if not x.startswith('https://www.google')]
#   links = [x for x in links if not x.startswith('https://www.google')]
#   links = [x for x in links if not x.startswith('https://www.google')]
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
