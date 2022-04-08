import os
import shutil
from google.colab import drive
from dirsync import sync
from rich.console import Console
console = Console()
from slugify import slugify
import configparser
import IPython

def configIN():
  import configparser
  import IPython
  config_file = "/content/config.ini"
  config = configparser.ConfigParser()
  config.read(config_file)

  #Set config values
  _weight     = config.getfloat("DEFAULT", "WEIGHT")
  _tv_weight  = config.getint("DEFAULT", "SMOOTH")
  _size       = config.getint("DEFAULT", "SIZE")
  _iterations = config.getint("DEFAULT", "RUN")
  _run_ini    = config.getint("DEFAULT", "RUN_INI")
  _save       = config.getint("DEFAULT", "SAVE")
  _rate       = config.getfloat("DEFAULT", "RATE")
  _decay      = config.getfloat("DEFAULT", "DECAY")
  _name       = config.get("DEFAULT", "NAME")

  setupMess3 = ['WEIGHT', 'SMOOTH', 'SIZE', 'RUN', 'RUN_INI', 'SAVE', 'RATE', 'DECAY']
  configValues = [_weight,_tv_weight,_size,_iterations,_run_ini,_save,_rate,_decay]

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
