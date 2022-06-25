  #@markdown <---------- Yeti // Functions

import os
import os.path
import time
import pandas as pd
from distutils.dir_util import copy_tree
from dirsync import sync
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
from IPython.display import display, Image
from rich.console import Console
import math


console = Console ( )

# --------------------------------------------------------------------FUNCTIONS
# CONSOLE
# -----------------------------------------------------------------------------
def txtH(action) :
    # -------------------------------------------------------------------------
    console.print ( f"[bright_white]{action}[/bright_white]" )


# -----------------------------------------------------------------------------
def txtL(action) :
    # -------------------------------------------------------------------------
    console.print ( f"[r black]{action}[/r black]" )


# -----------------------------------------------------------------------------
def txt(action , details) :
    # -------------------------------------------------------------------------
    console.print ( f"[bright_white]{action}[/bright_white] [r black]{details}[/r black]" )


# -----------------------------------------------------------------------------
def txtC(action , details) :
    # -------------------------------------------------------------------------
    console.print ( f"[bright_cyan]{action}[/bright_cyan] >> [r black]{details}[/r black]" )


# -----------------------------------------------------------------------------
def txtM(action , details) :
    # -------------------------------------------------------------------------
    console.print ( f"[bright_magenta]{action}[/bright_magenta] >> [r black]{details}[/r black]" )


# -----------------------------------------------------------------------------
def txtY(action , details) :
    # -------------------------------------------------------------------------
    console.print ( f"[bright_yellow]{action}[/bright_yellow] >> [r black]{details}[/r black]" )


# -----------------------------------------------------------------------------
def conSettings(project,init_image,quality,conf,gpu):
  # ---------------------------------------------------------------------------- 
    txtC('>> Project', project)
    txtC('>> Image', init_image)
    txtC('>> Quality', quality)
    txtC('>> Configs',conf)
    txtY('>> CUDA GPU ', gpu[1])


# -----------------------------------------------------------------------------    
def csv2ls(csv_file):
    # --------------------------------------------------------------------------
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        list1 = [rows[0] for rows in reader]

    return list1[1:]
      
# -----------------------------------------------------------------------------
def mk(path):
    # --------------------------------------------------------------------------
    if not os.path.exists (path):
      os.makedirs (path)

# -----------------------------------------------------------------------------
def imagePath(path) :
    # -------------------------------------------------------------------------
    """display each image in a path at 25% scale"""
    from IPython.display import Image , display
    for file in os.listdir ( path ) :
        if file.endswith ( "*.jpg" ) :
            txtH ( file )
            display ( Image ( filename = os.path.join ( path , file ) , width = 100 ) )


#-------------------------------------------------------------------------------
def montage(path , outpath) :
    #---------------------------------------------------------------------------
    file_paths = [ ]
    for root , directories , files in os.walk ( path ) :
        for filename in files :
            filepath = os.path.join ( root , filename )
            file_paths.append ( filepath )
            sorted(file_paths)
    montPaths = " ".join ( file_paths )
    montSettings = f"""-label '%f' -font Helvetica -pointsize 12 -background '#000000' -fill 'gray' -define jpeg:size=175x175 -geometry 175x175+2+2 -auto-orient {montPaths} {outpath}"""
    return montSettings , montPaths


# -----------------------------------------------------------------------------
def timeTaken(start_time) :
    # -----------------------------------------------------------------------------
    import time
    timeTakenFloat = "%s seconds" % (time.time ( ) - start_time)
    timeTaken = timeTakenFloat
    timeTaken_str = str ( timeTaken )
    timeTaken_split = timeTaken_str.split ( '.' )
    timeTakenShort = timeTaken_split [ 0 ] + '' + timeTaken_split [ 1 ] [ :0 ]
    txtM ( '>> Complete:' , f'{timeTakenShort} Seconds' )

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

#-------------------------------------------------------------------------------
def yeti(init_image , quality, gpu, conf, start_time, csv, threshMasks) :
    #---------------------------------------------------------------------------   
    #VARIABLES // Master
    #---------------------------------------------------------------------------  
    timeSlug = time.strftime("%H_%M")
    timeSlugConsole = time.strftime("%H:%M")
    init_file = os.path.basename(init_image)
    init_name = os.path.splitext(init_file)[0]
    #---------------------------------------------------------------------------
    project = init_name
    localPath = '/content'
    driveMount = '/mnt/drive'
    #---------------------------------------------------------------------------
    localPathIn = f'{localPath}/in'
    imagesOut = f'{localPath}/images_out'
    initPathIn = f'{localPathIn}/init'
    stylePathIn = f'{localPathIn}/style'
    promptPathIn = f'{localPathIn}/prompt'
    #---------------------------------------------------------------------------
    localPathOut = f'{localPath}/out/{project}'
    initPathOut = f'{localPathOut}/init'
    stylePathOut = f'{localPathOut}/style'
    maskPathOut = f'{localPathOut}/mask'
    framesPathOut = f'{localPathOut}/frames'
    finalPathOut = f'{localPathOut}/final'
    superPathOut = f'{localPathOut}/super'
    #---------------------------------------------------------------------------
    drivePath = f'{driveMount}/MyDrive/aida'
    drivePathIn = f'{drivePath}/in'
    drivePathOut = f'{drivePath}/out'
    driveOutProject = f'{drivePathOut}/{project}/{timeSlug}'
    #---------------------------------------------------------------------------
    configPath = f'{localPath}/config/'
    confPath = f'{configPath}/conf'
    configPathIn = f'{localPathIn}/config'
    confPathIn = f'{configPathIn}/conf'
    configPathOut = f'{localPathOut}/config'
    confPathOut = f'{configPathOut}/conf'
    #---------------------------------------------------------------------------
    montPathOut = f'{localPathOut}/contact'
    montFileMask = f'{montPathOut}/mask-contact_{project}.png'
    montFileFinal = f'{montPathOut}/final-contact_{project}.png'
    montFileSuper = f'{montPathOut}/super-contact_{project}.png'
    #---------------------------------------------------------------------------
    localPathsOut=['config','contact','init','prompt','frames','final','style','super']
    #---------------------------------------------------------------------------
    threshMasked=[]
    for i in threshMasks:
      threshMasked.append(f'{maskPathOut}/{project}-{i}_mask.jpg')
    
    #FOLDERS // Make local and drive OUT folders
    #---------------------------------------------------------------------------  
    otherPathsOut=[localPathIn,driveOutProject,confPath,maskPathOut]
    for path in otherPathsOut:
      mk(path)
    for path in (localPathsOut):
      mk(f'{localPathOut}/{path}')
    #CLEAN // Folders
    sample_data = '/content/sample_data'
    if os.path.isdir(sample_data):
        shutil.rmtree(sample_data)
    # --------------------------------------------------------------------------
    #SYNC // drive/in local/in
    sync(drivePathIn,localPathIn,'sync')
    shutil.copy(init_image,initPathOut)
    # --------------------------------------------------------------------------
    #WRITE Config //
    if quality=='test':
      _width=200
      _cut_outs=120
      _cut_pow=2.5
      _pixel_size=3
      _direct_init_weight=1
      _gradient_accumulation_steps=1
      _steps_per_scene=250
      _save_every=250
      _display_every=25
      _clear_every=50
      _scene_suffix=':1'
      _display_scale=1

      csv_file = f'{promptPathIn}/{csv}.csv'
      project = init_name
      df = pd.read_csv ( csv_file )
      col_names = list ( df.columns.values )
      for col in col_names :
          globals ( ) [ col ] = [ ]
          for value in df [ col ] :
              globals ( ) [ col ].append ( value )
      for names , preffixs , scenes , suffixs , styles in zip ( name , preffix , scene , suffix , style ) :
          confPath = configPathIn
          if not os.path.exists ( confPathOut ) :
              os.makedirs ( confPathOut )
          yaml = f'{confPathOut}/{names}.yaml'
          f = open ( yaml , 'w' )
          f.write ( """# @package _global_\n""" )
          f = open ( yaml , "a" )
          f.write (f"file_namespace: {names}\nscene_prefix: {preffixs}\nscenes: {scenes}\nwidth: {_width}\ncutouts: {_cut_outs}\ncut_pow: {_cut_pow}\npixel_size: {_pixel_size}\ndirect_init_weight: {_direct_init_weight}\ngradient_accumulation_steps: {_gradient_accumulation_steps}\nsteps_per_scene: {_steps_per_scene}\nsave_every: {_save_every}\ndisplay_every: {_display_every}\nclear_every: {_clear_every}\nscene_suffix: {_scene_suffix}\ndisplay_scale: {_display_scale}\n")
      for thresh in range ( 20 , 231 , 20 ) :
          img = cv2.imread ( init_image )
          os.makedirs ( maskPathOut , exist_ok = "True" )
          ret , img_binary = cv2.threshold ( img , thresh , 255 , cv2.THRESH_BINARY )
          imageio.imwrite ( f'{maskPathOut}/{project}-{thresh}_mask.jpg' , img_binary )
    
    clear_output()
    setupTime=timeTaken(start_time)
    # --------------------------------------------------------------------------
    return imagesOut,framesPathOut, threshMasked,configPath,confPath,init_image,montFileMask,timeSlug,timeSlugConsole,init_file,init_name,project,localPath,localPathIn, \
        configPathIn,confPathIn,initPathIn,stylePathIn,promptPathIn,localPathOut,configPathOut,\
        confPathOut,initPathOut,stylePathOut,maskPathOut,montPathOut,drivePath,drivePathIn,drivePathOut
    # --------------------------------------------------------------------------
