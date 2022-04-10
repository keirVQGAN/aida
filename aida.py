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

def config(file='/content/configAida.ini'):
  import configparser
  config_file = file
  config = configparser.ConfigParser()
  config.read(config_file)

def clone():
  sample_data='/content/sample_data'
  drive.mount('/mnt/drive')
  sync('/mnt/drive/MyDrive/aida/in', '/content/in', 'sync', create=True)
  os.makedirs('/content/out/contacts', exist_ok="True")
  os.makedirs('/content/out/archive', exist_ok="True")
  os.makedirs('/content/out/images', exist_ok="True")
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
    
def gif(lists,out,delay,scale):
  gifOut = f'/content/{out}.gif'
  !convert -delay $delay -resize $scale -loop 0 $lists $gifOut

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
