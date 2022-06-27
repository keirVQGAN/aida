# Yeti // Functions
import csv
import glob
import os
import os.path
import glob
import shutil
import time
import cv2
import imageio
import pandas as pd
from IPython.display import clear_output
from dirsync import sync
from rich.console import Console

console = Console()


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
    console.print(f"[bright_cyan]{action}[/bright_cyan] >> [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def txtM(action, details):
    # -------------------------------------------------------------------------
    console.print(f"[bright_magenta]{action}[/bright_magenta] >> [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def txtY(action, details):
    # -------------------------------------------------------------------------
    console.print(f"[bright_yellow]{action}[/bright_yellow] >> [r black]{details}[/r black]")

# -----------------------------------------------------------------------------
def conSettings(project, init_image, quality, conf, gpu):
    # ---------------------------------------------------------------------------- 
    txtC('>> Project', project)
    txtC('>> Image', init_image)
    txtC('>> Quality', quality)
    txtC('>> Configs', conf)
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
    if not os.path.exists(path):
        os.makedirs(path)

# -----------------------------------------------------------------------------
def imagePath(path):
    # -------------------------------------------------------------------------
    """display each image in a path at 25% scale"""
    from IPython.display import Image, display
    for file in os.listdir(path):
        if file.endswith("*.jpg"):
            txtH(file)
            display(Image(filename=os.path.join(path, file), width=100))

# -------------------------------------------------------------------------------
def montage(path, outpath):
    # ---------------------------------------------------------------------------
    file_paths = []
    for root, directories, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
            sorted(file_paths)
    montPaths = " ".join(file_paths)
    montSettings = f"""-label '%f' -font Helvetica -pointsize 12 -background '#000000' -fill 'gray' -define jpeg:size=175x175 -geometry 175x175+2+2 -auto-orient {montPaths} {outpath}"""
    return montSettings, montPaths

# -----------------------------------------------------------------------------
def timeTaken(start_time):
    # -----------------------------------------------------------------------------
    import time
    timeTakenFloat = "%s seconds" % (time.time() - start_time)
    timeTaken = timeTakenFloat
    timeTaken_str = str(timeTaken)
    timeTaken_split = timeTaken_str.split('.')
    timeTakenShort = timeTaken_split[0] + '' + timeTaken_split[1][:0]
    txtM('>> Complete:', f'{timeTakenShort} Seconds')

# -------------------------------------------------------------------
def copyExt(ext,src,dest):
    # -----------------------------------------------------------------
    for file_path in glob.glob(os.path.join(src, '**', ext), recursive=True):
        new_path = os.path.join(dest, os.path.basename(file_path))
        shutil.copy(file_path, new_path)

# -------------------------------------------------------------------
def moveExt(ext,src,dest):
    # -----------------------------------------------------------------
    for file_path in glob.glob(os.path.join(src, '**', ext), recursive=True):
        new_path = os.path.join(dest, os.path.basename(file_path))
        shutil.move(file_path, new_path)

# -------------------------------------------------------------------
def fps(video_file):
  # -------------------------------------------------------------------
    cap = cv2.VideoCapture(video_file)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return frame_count
