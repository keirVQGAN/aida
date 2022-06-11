
"""
AiDa.common v0.9 | Yeti - June 2022
"""

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------IMPORT
#SYSTEM
import os
import os.path
import sys
import shutil
import tarfile
#DATA
import re
import pandas as pd
import numpy as np
import csv
import time
#PATHS
from glob import glob
from dirsync import sync
from google.colab import drive
#CONSOLE
import IPython
from IPython.display import Image
from IPython.display import clear_output
from rich.console import Console
console = Console()
import cv2
import imageio
#--------------------------------------------------------------------FUNCTIONS
#CONSOLE
#-----------------------------------------------------------------------------
def txtH(action):
#-----------------------------------------------------------------------------
  console.print(f"[bright_white]{action}[/bright_white]")
#-----------------------------------------------------------------------------
def txtL(action):
#-----------------------------------------------------------------------------
  console.print(f"[r black]{action}[/r black]")
#-----------------------------------------------------------------------------
def txt(action, details):
#-----------------------------------------------------------------------------
  console.print(f"[bright_white]{action}[/bright_white] [r black]{details}[/r black]")
#-----------------------------------------------------------------------------
def txtC(action, details):
#-----------------------------------------------------------------------------
  console.print(f"[bright_cyan]{action}[/bright_cyan] > [r black]{details}[/r black]") 
#-----------------------------------------------------------------------------    
def txtM(action, details):
#-----------------------------------------------------------------------------
  console.print(f"[bright_magenta]{action}[/bright_magenta] > [r black]{details}[/r black]")
#-----------------------------------------------------------------------------
def txtY(action, details):
#-----------------------------------------------------------------------------
  console.print(f"[bright_yellow]{action}[/bright_yellow] > [r black]{details}[/r black]")
#-----------------------------------------------------------------------------
def conSettings(scene, image, style, quality, gpu, upScale):
#-----------------------------------------------------------------------------
  clear_output()
  txtC('>> Scene', scene)
  txtC('>> Image', image)
  txtC('>> Style', style)
  txtC('>> Quality', quality)
  txtY('>> CUDA GPU ', gpu[1])
  txtM('>> Synced', 'True')
  txtM('>> Upscaled', upScale)
  print('')
#-----------------------------------------------------------------------------
def conInstall(timeSlugConsole, gpu, _scenes, _init_image, _style, _quality, _upScale):
#-----------------------------------------------------------------------------
  clear_output()
  txtL(f'>> SETUP COMPLETE @ {timeSlugConsole}')
  txtC('>> Installed ','AiDa.common')
  txtC('>> Installed ','AiDa.txt2img')
  txtC('>> Installed ','AiDa.super')
  txtC('>> CUDA GPU0 ', gpu[1])
  txtY('>> Scene',_scenes)
  txtY('>> Image',_init_image)
  txtY('>> Style',_style)
  txtM('>> Quality',_quality)
  txtM('>> Upscale ',_upScale)
#-----------------------------------------------------------------------------
def mount():
#-----------------------------------------------------------------------------
  drive.mount('/mnt/drive')
#-----------------------------------------------------------------------------
def syncDir(source, target):
#-----------------------------------------------------------------------------
  sync(source, target, 'sync', create=True)
#-----------------------------------------------------------------------------
def rm(dir):
#-----------------------------------------------------------------------------
  shutil.rmtree(dir)
#-----------------------------------------------------------------------------
def cp(filename,target):
#-----------------------------------------------------------------------------
  shutil.copyfile(file,dest)   
#-----------------------------------------------------------------------------
def mk(dir):
#-----------------------------------------------------------------------------
  os.makedirs(dir, exist_ok="True")
#-----------------------------------------------------------------------------
def lsDir(dir):
#-----------------------------------------------------------------------------
  return [os.path.join(dir, file) for file in os.listdir(dir)]
#-----------------------------------------------------------------------------
def ls(dir):
#-----------------------------------------------------------------------------
  return [os.path.join(dir, file) for file in os.listdir(dir)]
#-----------------------------------------------------------------------------
def ls2str(ls):
#-----------------------------------------------------------------------------
  return " ".join(ls)
#-----------------------------------------------------------------------------
def name(file_path):
#-----------------------------------------------------------------------------
  basename = os.path.basename(file_path)
  file_name = os.path.splitext(basename)[0]
  return file_name
#-----------------------------------------------------------------------------
def zip(filename, source):
#-----------------------------------------------------------------------------
  with tarfile.open(filename, "w:gz") as tar:
      tar.add(source, arcname=os.path.basename(source))
#-----------------------------------------------------------------------------
def uzip(filename, target):
#-----------------------------------------------------------------------------
  my_tar = tarfile.open(filename)
  my_tar.extract(target)
  my_tar.close()
#-----------------------------------------------------------------------------
def timeTaken(start_time):
#-----------------------------------------------------------------------------
  import time
  timeTakenFloat = "%s seconds" % (time.time() - start_time)
  timeTaken = timeTakenFloat
  timeTaken_str = str(timeTaken)
  timeTaken_split = timeTaken_str.split('.')
  timeTakenShort = timeTaken_split[0] + '' + timeTaken_split[1][:0]
  txtM('>> Complete: ',f'{timeTakenShort} Seconds')
#-----------------------------------------------------------------------------
def clone():
#-----------------------------------------------------------------------------
  sample_data=os.path.isdir('/content/sample_data')
  drive.mount('/mnt/drive')
  sync('/mnt/drive/MyDrive/aida/in', '/content/in', 'sync', create=True)
  os.makedirs('/content/out/', exist_ok="True")
  os.makedirs('/content/aida/txt2img', exist_ok="True")
  sync('/content/in/config', '/content/out/txt2img/config', 'sync', create=True)
  shutil.rmtree('/content/in/config')
  if sample_data==1:
    shutil.rmtree('/content/sample_data')
#-----------------------------------------------------------------------------
def preProcess(_project,_init_image,_scenes,_quality,_imageOut):
#-----------------------------------------------------------------------------
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
  mk(_imageOut)
#-----------------------------------------------------------------------------
def syncOut(
#-----------------------------------------------------------------------------
  localPath,
  localOut,
  driveOut,
  ):
  mk(localOut)
  for root, dirs, files in os.walk(localPath):
      for name in files:
          if name.endswith(".png"):
              shutil.copy(os.path.join(root, name), localOut)

  syncDir(localOut,driveOut)
#-----------------------------------------------------------------------------
def test(_scenes,_project,_style,_init_image):
#-----------------------------------------------------------------------------
  import imageio
  import csv
  _confLs=[]
  for _thresh in range(20, 231, 20):
    #make masks
    maskPath=f'/content/in/mask/{_project}'
    confPath=f'/content/out/txt2img/config/conf'
    img = cv2.imread(_init_image)
    os.makedirs(maskPath, exist_ok="True")
    ret, img_binary = cv2.threshold(img, _thresh, 255, cv2.THRESH_BINARY)
    imageio.imwrite(f'{maskPath}/{_project}_mask{_thresh}.jpg',img_binary) 
    _thresh = str(_thresh)
    _yaml = f'{confPath}/{_project}_mask{_thresh}.yaml'
    f = open(_yaml, "a")
    f.write(f"""#@package _global_
    scenes: {_scenes}
    init_image: {_init_image}
    file_namespace: {_project}_mask{_thresh}
    scene_suffix: :0.8_[/content/in/mask/{_project}/{_project}_mask{_thresh}.jpg]
    direct_image_prompts: {_style}:0.6
    steps_per_scene: 150
    save_every: 150
    width: 200
    cutouts: 22
    cut_pow: 2
    pixel_size: 3
    gradient_accumulation_steps: 1""")
    _confLs.append(_yaml)
    f.close()
#-----------------------------------------------------------------------------
def draft(_scenes,_project,_style,_init_image):
#-----------------------------------------------------------------------------
  import imageio
  import csv
  _confLs=[]
  for _thresh in range(20, 231, 20):
    #make masks
    maskPath=f'/content/in/mask/{_project}'
    confPath=f'/content/out/txt2img/config/conf'
    img = cv2.imread(_init_image)
    os.makedirs(maskPath, exist_ok="True")
    ret, img_binary = cv2.threshold(img, _thresh, 255, cv2.THRESH_BINARY)
    imageio.imwrite(f'{maskPath}/{_project}_mask{_thresh}.jpg',img_binary) 
    _thresh = str(_thresh)
    _yaml = f'{confPath}/{_project}_mask{_thresh}.yaml'
    f = open(_yaml, "a")
    f.write(f"""#@package _global_
    scenes: {_scenes}
    file_namespace: {_project}_mask{_thresh}
    scene_suffix: :0.8_[/content/in/mask/{_project}/{_project}_mask{_thresh}.jpg]
    direct_image_prompts: {_style}:0.8
    steps_per_scene: 1000
    save_every: 1000
    width: 200
    cutouts: 230
    cut_pow: 2.7
    pixel_size: 3
    gradient_accumulation_steps: 2""")
    _confLs.append(_yaml)
    f.close()
#-------------------------------------------------------------------------------
def merge(_imageSuperPath, _project, _scenes, _init_image):
#-----------------------------------------------------------------------------
  #GET FILE LIST OF UPSCALES IMAGES
  _imageSuperLs = []
  for root, dirs, files in os.walk(_imageSuperPath):
      for name in files:
          if name.endswith(".png"):
            a = os.path.join(root, name)
            _imageSuperLs.append(a)

  _imageOutStr = ':0.2|'.join(_imageSuperLs)
  #MAKE YML // conf/merge.yml
  _yaml = f'/content/out/txt2img/config/conf/{_project}_merge.yaml'
  if os.path.isfile(_yaml):
    os.remove(_yaml)
  f = open(_yaml, "a")
  f.write(f"""#@package _global_
  scenes: {_scenes}
  file_namespace: {_project}_merge
  direct_image_prompts: {_imageOutStr}
  steps_per_scene: 1500
  save_every: 1500
  width: 200
  cutouts: 230
  cut_pow: 2.8
  pixel_size: 3
  gradient_accumulation_steps: 2""")
  f.close()
#-------------------------------------------------------------------------------
def mergeTest(_imageSuperPath, _project, _scenes, _init_image):
#-----------------------------------------------------------------------------
  #GET FILE LIST OF UPSCALES IMAGES
  _imageSuperLs = []
  for root, dirs, files in os.walk(_imageSuperPath):
      for name in files:
          if name.endswith(".png"):
            a = os.path.join(root, name)
            _imageSuperLs.append(a)

  _imageOutStr = ':0.2|'.join(_imageSuperLs)
  #MAKE YML // conf/merge.yml
  _yaml = f'/content/out/txt2img/config/conf/{_project}_merge.yaml'
  if os.path.isfile(_yaml):
    os.remove(_yaml)
  f = open(_yaml, "a")
  f.write(f"""#@package _global_
  scenes: {_scenes}
  file_namespace: {_project}_merge
  direct_image_prompts: {_imageOutStr}
  steps_per_scene: 300
  save_every: 300
  width: 200
  cutouts: 32
  cut_pow: 2.5
  pixel_size: 3
  gradient_accumulation_steps: 1""")
  f.close()
