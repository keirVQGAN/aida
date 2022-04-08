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

def setup(renderer):
    from dirsync import sync
    localDir = '/content/in'
    remoteDir = f'/mnt/drive/MyDrive/aida/renderer/{renderer}/setup'
    drive.mount('/mnt/drive')
    os.makedirs(localDir, exist_ok="True")
    sync(remoteDir, localDir, 'sync', create=True)

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
    
def gpu():
    !nvidia - smi


def cpu():
    info = ["Model name:", "L3 cache:"]
    for ob in info:
        !lscpu | grep
        "$ob"
    !nvidia - smi
    
def img(image, scale):
    image_show = cv2.imread(image, cv2.IMREAD_UNCHANGED)
    scale_percent = scale  # percent of original size
    width_show = int(image_show.shape[1] * scale_percent / 100)
    height_show = int(image_show.shape[0] * scale_percent / 100)
    dim = (width_show, height_show)
    resized = cv2.resize(image_show, dim, interpolation=cv2.INTER_AREA)
    cv2_imshow(resized)
