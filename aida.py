"""
AiDa.common v0.9 | Yeti - June 2022
"""

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------IMPORT
#//SYSTEM
import os
import os.path
#//DATA
import pandas as pd

#//PATHS & FILES
from dirsync import sync
from distutils.dir_util import copy_tree
from google.colab import drive
import glob
import shutil
import tarfile
#//RICH CONSOLE
from IPython.display import clear_output
from rich.console import Console
console = Console()
#//IMAGES
import imageio
import cv2
import csv
import re
import time
import openai
from PIL import Image
from PIL import ImageFile

# --------------------------------------------------------------------FUNCTIONS
# CONSOLE
# -----------------------------------------------------------------------------
def txtH(action):
    # -----------------------------------------------------------------------------
    console.print(f"[bright_white]{action}[/bright_white]")

# -----------------------------------------------------------------------------
def txtL(action):
    # -----------------------------------------------------------------------------
    console.print(f"[r black]{action}[/r black]")

# -----------------------------------------------------------------------------
def txt(action, details):
    # -----------------------------------------------------------------------------
    console.print(f"[bright_white]{action}[/bright_white] [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def txtC(action, details):
    # -----------------------------------------------------------------------------
    console.print(f"[bright_cyan]{action}[/bright_cyan] > [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def txtM(action, details):
    # -----------------------------------------------------------------------------
    console.print(f"[bright_magenta]{action}[/bright_magenta] > [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def txtY(action, details):
    # -----------------------------------------------------------------------------
    console.print(f"[bright_yellow]{action}[/bright_yellow] > [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def mount():
    # -----------------------------------------------------------------------------
    drive.mount('/mnt/drive')

# -----------------------------------------------------------------------------
def syncDir(source, target):
    # -----------------------------------------------------------------------------
    sync(source, target, 'sync', create=True)

# -----------------------------------------------------------------------------
def rm(dir):
    # -----------------------------------------------------------------------------
    shutil.rmtree(dir)

# -----------------------------------------------------------------------------
def cp(filename, target):
    # -----------------------------------------------------------------------------
    shutil.copyfile(file, dest)

# -----------------------------------------------------------------------------
def mk(dir):
    # -----------------------------------------------------------------------------
    os.makedirs(dir, exist_ok="True")

# -----------------------------------------------------------------------------
def lsDir(dir):
    # -----------------------------------------------------------------------------
    return [os.path.join(dir, file) for file in os.listdir(dir)]

# -----------------------------------------------------------------------------
def ls(dir):
    # -----------------------------------------------------------------------------
    return [os.path.join(dir, file) for file in os.listdir(dir)]

# -----------------------------------------------------------------------------
def ls2str(ls):
    # -----------------------------------------------------------------------------
    return " ".join(ls)

# -----------------------------------------------------------------------------
def cvs2str(file_name):
    # -----------------------------------------------------------------------------
    with open(file_name, 'r') as file_obj:
        csv_reader = csv.DictReader(file_obj)
        string = ''
        for row in csv_reader:
            if row['project_id'] == row['project_id']:
                string += '{}\n'.format(row['project_id'])
        return string

# -----------------------------------------------------------------------------
def name(file_path):
    # -----------------------------------------------------------------------------
    basename = os.path.basename(file_path)
    file_name = os.path.splitext(basename)[0]
    return file_name


# -----------------------------------------------------------------------------
def zip(filename, source):
    # -----------------------------------------------------------------------------
    with tarfile.open(filename, "w:gz") as tar:
        tar.add(source, arcname=os.path.basename(source))


# -----------------------------------------------------------------------------
def uzip(filename, target):
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    my_tar = tarfile.open(filename)
    my_tar.extract(target)
    my_tar.close()


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

    
#-------------------------------------------------------------------
def copyExt(
#-------------------------------------------------------------------
    ext,
    src,
    dest):
  #-----------------------------------------------------------------
    for file_path in glob.glob(os.path.join(src, '**', ext), recursive=True):
        new_path = os.path.join(dest, os.path.basename(file_path))
        shutil.copy(file_path, new_path)

        
# ------------------------------------------------------------------------------
################################################################################
# yeti.txt2img
################################################################################
# ------------------------------------------------------------------------------
################################################################################
# SETUP
# ------------------------------------------------------------------------------
def clone():
  # ----------------------------------------------------------------------------
    sample_data = os.path.isdir('/content/sample_data')
    os.makedirs('/content/out/', exist_ok="True")
    os.makedirs('/content/in/', exist_ok="True")
    os.makedirs('/content/aida/txt2img', exist_ok="True")
    drive.mount('/mnt/drive', force_remount=False)
    sync('/mnt/drive/MyDrive/aida/in', '/content/in', 'sync')
    
    copy_tree('/content/in/config', '/content/out/txt2img/config')
    shutil.rmtree('/content/in/config')
    if sample_data == 1:
        shutil.rmtree('/content/sample_data')
        
        
# ------------------------------------------------------------------------------
def preProcess(csv_file, init_image, quality):
  # ----------------------------------------------------------------------------
  init_file = os.path.basename(init_image)
  init_name = os.path.splitext(init_file)[0]
  _project=init_name
  maskPath = f'/content/in/mask/{_project}'
  confPath = f'/content/out/txt2img/config/conf'
  if not os.path.isdir('/content/in'):
    clone()
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
      yaml=f'{confPath}{_project}-{names}.yaml'
      f = open(yaml, 'w')
      f.write("""#@package _global \n""")
      f = open(yaml, "a")
      f.write(f"filenamespace: {_project}-{names}\ninit_image: {init_image}\nscene_preffix: {preffixs}\nscenes: {scenes}\nscene_suffix: {suffixs}\nquality: {quality}")
      #

  for _thresh in range(20, 231, 20):
    img = cv2.imread(init_image)
    os.makedirs(maskPath, exist_ok="True")
    ret, img_binary = cv2.threshold(img, _thresh, 255, cv2.THRESH_BINARY)
    imageio.imwrite(f'{maskPath}/{_project}_mask{_thresh}.jpg', img_binary)
    _thresh = str(_thresh)
  return _project

 sleep
    

################################################################################
# RENDER
# ------------------------------------------------------------------------------
def render(conf=_conf)
# ------------------------------------------------------------------------------
    renderSettings=f'-m pytti.workhorse --multirun conf={_conf}'
    return renderSettings


# ------------------------------------------------------------------------------
def renderOveride(conf=_conf)
# ------------------------------------------------------------------------------
    renderSettings=f'-m pytti.workhorse --multirun conf={_conf} scenes={scenes} scene_preffix={scene_preffix} scene_suffix={scene_suffix} steps_per_scene={steps_per_scene} direct_image_prompt= save_every={save_every} width={width} cutouts={cutouts} cut_pow={cut_pow} pixel_size={pixel_size} gradient_accumulation_steps={gradient_accumulation_steps} '
    return renderSettings



################################################################################
# POST
#-----------------------------------------------------------------
def syncPost(
#----------------------------------------------------------------- 
    _imageRender,
    _init_image,
    _style,
    _project,
    _steps
):
#-----------------------------------------------------------------
    timeSlug = time.strftime("%H_%M")
    _drivePath='/mnt/drive/MyDrive/aida'
    _driveOut=f'{_drivePath}/out/{_project}/{timeSlug}'
    _driveInPath=f'{_driveOut}/in/'
    _driveOutPath=f'{_driveOut}/out/'
    configPath='/content/out/txt2img/config'
    maskPath=f'/content/in/mask/{_project}'
    outFrames=f'{_driveOutPath}frames'
    outFinal=f'{_driveOutPath}/final/'


    outInit=f'{_driveInPath}/init/'
    outStyle=f'{_driveInPath}/style'
    outConfig=f'{_driveInPath}config/'
    outMask=f'{_driveInPath}/mask/' 
    inPathList = ['init','style','config/conf','mask',]
    outPathList = ['frames','final','super']

    os.makedirs(_driveOut, exist_ok="True")
    
    for items in inPathList:
        path = os.path.join(_driveInPath, items)
        os.makedirs(path, exist_ok="True")

    for items in outPathList:
        path = os.path.join(_driveOutPath, items)
        os.makedirs(path, exist_ok="True")

    #-----------------------------------------------------------------
    #SYNC // IN
    shutil.copy(_init_image, f'{_driveInPath}/init/')
    shutil.copy(_style, f'{_driveInPath}/style/')
    copy_tree(configPath, outConfig)
    copy_tree(maskPath, outMask) 
    # #SYNC // OUT
    _ext=f'*.png'
    copyExt(_ext,_imageRender,outFrames)
    _ext=f'*{_steps}.png'
    copyExt(_ext,_imageRender,outFinal)
    rm(_imageRender)
    
# ------------------------------------------------------------------------------
################################################################################
# CONSOLE
    
# -----------------------------------------------------------------------------
def conSettings(scene, image, style, quality, gpu, upScale):
    # -----------------------------------------------------------------------------
    clear_output()
    txtC('>> Scene', scene)
    txtC('>> Image', image)
    txtC('>> Style', style)
    txtC('>> Quality', quality)
    txtY('>> CUDA GPU ', gpu[1])
    txtM('>> Synced', 'True')
    txtM('>> Upscaled', upScale)
    print('')


# -----------------------------------------------------------------------------
def conInstall(timeSlugConsole, gpu, _scenes, _init_image, _style, _quality, _upScale):
    # -----------------------------------------------------------------------------
    clear_output()
    txtL(f'>> SETUP COMPLETE @ {timeSlugConsole}')
    txtC('>> Installed ', 'AiDa.common')
    txtC('>> Installed ', 'AiDa.txt2img')
    txtC('>> Installed ', 'AiDa.super')
    txtC('>> CUDA GPU0 ', gpu[1])
    txtY('>> Scene', _scenes)
    txtY('>> Image', _init_image)
    txtY('>> Style', _style)
    txtM('>> Quality', _quality)
    txtM('>> Upscale ', _upScale)
