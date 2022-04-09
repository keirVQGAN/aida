import cv2
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

def config(file='/content/configAida.ini'):
  import configparser
  config_file = file
  config = configparser.ConfigParser()
  config.read(config_file)

def clone():
  sample_data='/content/sample_data'
  drive.mount('/mnt/drive')
  sync('/mnt/drive/MyDrive/aida/in', '/content/in', 'sync', create=True)
  os.makedirs('/content/out/complete', exist_ok="True")
  if sample_data==1:
      shutil.rmtree('/content/sample_data') 

def txtH(action):
    console.print(f"[bold_white]{action}[/bold_white]")

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

def name(path):
    return os.path.basename(path)

def name_time(file):
    times = time.strftime("%H-%M-%S")
    file = f'{file}_{times}'
    return file

def slug(path):
    path_file = os.path.basename(path)
    times = time.strftime("%H-%M-%S")
    path_file_time = f'{path_file}_{times}'
    return path_file_time
    

# */ Clean -> Get file as slug *\
def slug(text):
    t = slugify(text, entities=True, decimal=True, hexadecimal=True, max_length=0, word_boundary=False, separator='_',
                save_order=False, stopwords=(), regex_pattern=None, lowercase=True, replacements=(),
                allow_unicode=False)
    return t

# */ Clean -> Get files without path *\
def filename(file):
    parts = file.rpartition('.')
    if len(parts) > 1:
        return ''.join(parts[:-1]).rstrip('.') if parts[0] else file
    else:
        return file
