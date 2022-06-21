#@markdown <---------- Yeti // Functions
from dirsync import sync
import os
import os.path
import time
import pandas as pd
from distutils.dir_util import copy_tree
from google.colab import drive
import glob
import shutil
import tarfile
from IPython.display import clear_output
import imageio
import cv2
import csv
import re
import time
from PIL import Image
from PIL import ImageFile
from IPython.display import clear_output
console=Console()

# --------------------------------------------------------------------FUNCTIONS
# CONSOLE
# -----------------------------------------------------------------------------
def txtH(action):
    # -------------------------------------------------------------------------
    console.print(f"[bright_white]{action}[/bright_white]")

# -----------------------------------------------------------------------------
def txtL(action):
    # -------------------------------------------------------------------------
    console.print(f"[r black]{action}[/r black]")

# -----------------------------------------------------------------------------
def txt(action, details):
    # -------------------------------------------------------------------------
    console.print(f"[bright_white]{action}[/bright_white] [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def txtC(action, details):
    # -------------------------------------------------------------------------
    console.print(f"[bright_cyan]{action}[/bright_cyan] > [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def txtM(action, details):
    # -------------------------------------------------------------------------
    console.print(f"[bright_magenta]{action}[/bright_magenta] > [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def txtY(action, details):
    # -------------------------------------------------------------------------
    console.print(f"[bright_yellow]{action}[/bright_yellow] > [r black]{details}[/r black]")

   
# -----------------------------------------------------------------------------
def timeTaken(start_time):
    # -----------------------------------------------------------------------------
    import time
    timeTakenFloat = "%s seconds" % (time.time() - start_time)
    timeTaken = timeTakenFloat
    timeTaken_str = str(timeTaken)
    timeTaken_split = timeTaken_str.split('.')
    timeTakenShort = timeTaken_split[0] + '' + timeTaken_split[1][:0]
    txtM('>> Complete: ', f'{timeTakenShort} Seconds')

def yeti(init_image, quality):
  #-------------------------------------------------------------------------------
  #MOUNT // Drive
  driveMount='/mnt/drive'
  drive.mount('/mnt/drive')
  #-------------------------------------------------------------------------------
  #VARIABLES // Master
  localPath='/content'
  localPathIn = f'{localPath}/in'
  localPathAida = f'{localPath}/aida'
  localPathTxt2Img = f'{localPathAida}/txt2img'
  #-------------------------------------------------------------------------------
  configPathIn = f'{localPathIn}/config'
  initPathIn=f'{localPathIn}/init'
  stylePathIn=f'{localPathIn}/style'
  promptPathIn=f'{localPathIn}/prompt'
  #-------------------------------------------------------------------------------
  localPathOut = f'{localPath}/out'
  #-------------------------------------------------------------------------------
  configPathOut = f'{localPathOut}/txt2img/config'
  confPathOut = f'{configPathOut}/conf'
  initPathOut=f'{localPathOut}/init'
  stylePathOut=f'{localPathOut}/style'
  maskPathOut=f'{localPathOut}/mask'
  localPathTxt2ImgOut = f'{localPathOut}/txt2img'
  localPathMultirun = f'{localPathTxt2ImgOut}/multirun'
  #-------------------------------------------------------------------------------
  drivePath=f'{driveMount}/MyDrive/aida'
  drivePathIn = f'{drivePath}/in'
  drivePathOut = f'{drivePath}/out'
  #-------------------------------------------------------------------------------
  configPathDrive = f'{drivePathIn}/config'
  initPathDrive=f'{drivePathIn}/init'
  stylePathDrive=f'{drivePathIn}/style'
  maskPathDrive=f'{drivePathIn}/mask'
  promptPathDrive=f'{drivePathIn}/prompt'
  #-------------------------------------------------------------------------------
  projectPaths=[driveMount,localPathIn,localPathAida,localPathTxt2Img,localPath,configPathIn,initPathIn,stylePathIn,promptPathIn,localPathOut,localPathMultirun,localPathTxt2ImgOut,confPathOut,configPathOut,initPathOut,stylePathOut,maskPathOut,drivePath,drivePathIn,drivePathOut,configPathDrive,initPathDrive,stylePathDrive,maskPathDrive,promptPathDrive]
  # ----------------------------------------------------------------------------

  for path in projectPaths:
    if not os.path.exists(path):
        os.makedirs(path)

  sample_data='/content/sample_data'
  if os.path.isdir(sample_data):
    shutil.rmtree(sample_data)

  #SYNC
  sync(drivePathIn, localPathIn, 'sync')
  sync(configPathIn,configPathOut, 'sync')

  
# ------------------------------------------------------------------------------
  # ----------------------------------------------------------------------------
  timeSlug = time.strftime("%H_%M")
  timeSlugConsole = time.strftime("%H:%M")
  init_file = os.path.basename(init_image)
  init_name = os.path.splitext(init_file)[0]
  maskPath=maskPathOut
  confPath=confPathOut
  csv_file='/content/in/prompt/made_of.csv'
  project=init_name
  df = pd.read_csv(csv_file)
  col_names = list(df.columns.values)
  for col in col_names:
    globals()[col] = []
    for value in df[col]:
        globals()[col].append(value)
  for names,preffixs,scenes,suffixs,styles in zip(name,preffix,scene,suffix,style):
      confPath='/content/out/txt2img/config/conf/'
      if not os.path.exists(confPath):
        os.makedirs(confPath)
      yaml=f'{confPath}{project}-{names}.yaml'
      f = open(yaml, 'w')
      f.write("""#@package _global \n""")
      f = open(yaml, "a")
      f.write(f"filenamespace: {project}-{names}\ninit_image: {init_image}\nscene_preffix: {preffixs}\nscenes: {scenes}\nscene_suffix: {suffixs}\nquality: {quality}")
  
  init_file = os.path.basename(init_image)
  init_name = os.path.splitext(init_file)[0]
  project=init_name
  drivePathOutFrames = f'{drivePathOut}/{project}/{timeSlug}/frames'
  drivePathOutFinal = f'{drivePathOut}/{project}/{timeSlug}/final'
  drivePathOutSuper = f'{drivePathOut}/{project}/{timeSlug}/super'
  drivePathOutMerged = f'{drivePathOut}/{project}/{timeSlug}/merged'
  drivePathOutSettings = f'{drivePathOut}/{project}/{timeSlug}/settings'

  for thresh in range(20, 231, 20):
    maskPath = maskPathOut
    img = cv2.imread(init_image)
    os.makedirs(maskPath, exist_ok="True")
    ret, img_binary = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    imageio.imwrite(f'{maskPath}/{project}_mask{thresh}.jpg', img_binary)

  shutil.copy(init_image,initPathOut)
  
  return driveMount,localPathIn,localPathAida,localPathTxt2Img,localPath,configPathIn,initPathIn,stylePathIn,promptPathIn,localPathOut,localPathMultirun,localPathTxt2ImgOut,confPathOut,configPathOut,initPathOut,stylePathOut,maskPathOut,drivePath,drivePathIn,drivePathOut,configPathDrive,initPathDrive,stylePathDrive,maskPathDrive,promptPathDrive,projectPaths,project
