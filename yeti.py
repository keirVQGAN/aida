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

# -------------------------------------------------------------------------------
def yeti(init_image, initVid, yetiVideo, yetiMerge, useMasks, quality, gpu, start_time, csv, threshMasks):
    # ---------------------------------------------------------------------------  
    timeSlug = time.strftime("%H")                     #VARIABLE // timeSlug
    timeSlugConsole = time.strftime("%H:%M")
    null = None                                           #REQUIRED FOR WORKHORSE
    true = True                                           #REQUIRED FOR WORKHORSE
    false = False                                         #REQUIRED FOR WORKHORSE
    # ---------------------------------------------------------------------------
    localPath = '/content'                                #VARIABLE // root paths
    driveMount = '/mnt/drive'
    init_file = os.path.basename(init_image)
    init_name = os.path.splitext(init_file)[0]
    project = init_name
    # ---------------------------------------------------------------------------
    localPathIn = f'{localPath}/in'                          #VARIABLE // localIN
    imagesOut = f'{localPath}/images_out'
    initPathIn = f'{localPathIn}/init'
    initVidPathIn = f'{localPathIn}/initVid'
    stylePathIn = f'{localPathIn}/style'
    promptPathIn = f'{localPathIn}/prompt'
    # ---------------------------------------------------------------------------
    localPathOut = f'{localPath}/out/{project}'             #VARIABLE // localOUT
    initPathOut = f'{localPathOut}/init'
    stylePathOut = f'{localPathOut}/style'
    maskPathOut = f'{localPathOut}/mask'
    framesPathOut = f'{localPathOut}/frames'
    finalPathOut = f'{localPathOut}/final'
    superPathOut = f'{localPathOut}/super'
    settingsPathOut = f'{localPathOut}/super'
    # ---------------------------------------------------------------------------
    drivePath = f'{driveMount}/MyDrive/aida'                #VARIABLE // driveOUT
    drivePathIn = f'{drivePath}/in'
    drivePathOut = f'{drivePath}/out'
    driveOutProject = f'{drivePathOut}/{timeSlug}-00/{project}/'
    # ---------------------------------------------------------------------------
    configPath = f'{localPath}/config/'                  #VARIABLE // configPaths
    confPath = f'{configPath}/conf'
    configPathIn = f'{localPathIn}/config'
    confPathIn = f'{configPathIn}/conf'
    configPathOut = f'{localPathOut}/config'
    confPathOut = f'{configPathOut}/conf'
    # ---------------------------------------------------------------------------
    montPathOut = f'{localPathOut}/contact'
    montFileMask = f'{montPathOut}/mask-contact_{project}.png'
    montFileFrames = f'{montPathOut}/frames-contact_{project}.png'
    montFileFinal = f'{montPathOut}/final-contact_{project}.png'
    montFileSuper = f'{montPathOut}/super-contact_{project}.png'

    # ---------------------------------------------------------------------------
    localPathsOut = ['config', 'contact', 'init', 'prompt', 'frames', 'final', 'style', 'super','mask','settings']
    otherPathsOut = [localPathIn, driveOutProject, confPath, maskPathOut]
    # --------------------------------------------------------------------------
    csv_file = f'{promptPathIn}/{csv}.csv'

    CONFIG_BASE_PATH = "config"
    CONFIG_DEFAULTS = "default.yaml"
    # --------------------------------------------------------------------------
    #QUALITY SETTINGS
    if quality == 'test':
        _width = 250
        _cut_outs = 160
        _cut_pow = 2.6
        _pixel_size = 2
        _direct_init_weight = 0.4
        _gradient_accumulation_steps = 2
        _steps_per_scene = 1250
        _save_every = 25
        _display_every = 25
        _clear_every = 50
        _display_scale = 1
        
    if quality == 'draft':
        _width = 200
        _cut_outs = 120
        _cut_pow = 2.7
        _pixel_size = 3
        _direct_init_weight = 1.5
        _gradient_accumulation_steps = 2
        _steps_per_scene = 2000
        _save_every = 10
        _display_every = 50
        _clear_every = 100
        _scene_suffix = ':1'
        _display_scale = 0.75
        
    if quality == 'proof':
        _width = 200
        _cut_outs = 220
        _cut_pow = 2.8
        _pixel_size = 3
        _direct_init_weight = 1.5
        _gradient_accumulation_steps = 2
        _steps_per_scene = 2000
        _save_every = 2000
        _display_every = 1000
        _clear_every = 2000
        _display_scale = 0.75

    if yetiVideo:
        _animation_mode= 'Video Source'
        _width = 500
        _cut_outs = 20
        _cut_pow = 2
        _pixel_size = 1
        _direct_init_weight = 2
        _gradient_accumulation_steps = 1
        _steps_per_scene = fps(initVid)
        _save_every = 1
        _display_every = 10
        _clear_every = 10
        _scene_suffix = ':0.7'
        _display_scale = 1
        _interpolation_steps = 1
        _video_path = f'{initVid}'
        _frame_stride = 30
        _reencode_each_frame = true
        _frames_per_second = 30
        # _flow_long_term_samples=0

    finalStep = _steps_per_scene / _save_every
    finalStep = int(finalStep)
    finalList=[]

    # ---------------------------------------------------------------------------   
    # FOLDERS // Make local and drive OUT folders
    for path in otherPathsOut: mk(path)
    for path in (localPathsOut): mk(f'{localPathOut}/{path}')
    sample_data = '/content/sample_data'
    if os.path.isdir(sample_data): shutil.rmtree(sample_data)
        
    # --------------------------------------------------------------------------
    # WRITE // Threshold Masks
    threshMasked = []
    for thresh in range(20, 221, 10):
        img = cv2.imread(init_image)
        ret, img_binary = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
        imageio.imwrite(f'{maskPathOut}/{project}-{thresh}_mask.jpg', img_binary)
        threshMasked.append(f'{maskPathOut}/{project}-{thresh}_mask.jpg')
        
    # --------------------------------------------------------------------------
    # MAKE yaml from csv
    df = pd.read_csv(csv_file)
    col_names = list(df.columns.values)
    for col in col_names:
        globals()[col] = []
        for value in df[col]:
            globals()[col].append(value)            
    for names, preffixs, scenes, suffixs, styles in zip(name, preffix, scene, suffix, style):
        yaml = f'{confPath}/{names}.yaml'
        if yetiVideo:
            yaml_settings = f"""# @package _global_\nfile_namespace: {names}\nscene_prefix: {preffixs} \nscenes: {scenes}\nwidth: {_width}\ncutouts: {_cut_outs}\ncut_pow: {_cut_pow}\npixel_size: {_pixel_size}\ndirect_init_weight: {_direct_init_weight}\nsteps_per_scene: {_steps_per_scene}\nsave_every: {_save_every}\ndisplay_every: {_display_every}\nclear_every: {_clear_every}z\nscene_suffix: {suffixs}\ndisplay_scale: {_display_scale}\nanimation_mode: {_animation_mode}\nvideo_path: '{_video_path}'\nframe_stride: {_frame_stride}\ndirect_image_prompt: ''\ninit_image: ''\nframes_per_second: {_frames_per_second}"""
        else:
            yaml_settings = f"""# @package _global_\nfile_namespace: {names}-{quality}\nscene_prefix: {preffixs} \nscenes: {scenes}\nwidth: {_width}\ncutouts: {_cut_outs}\ncut_pow: {_cut_pow}\npixel_size: {_pixel_size}\ndirect_init_weight: {_direct_init_weight}\ngradient_accumulation_steps: {_gradient_accumulation_steps}\nsteps_per_scene: {_steps_per_scene}\nsave_every: {_save_every}\ndisplay_every: {_display_every}\nclear_every: {_clear_every}\nscene_suffix: {suffixs}\ndisplay_scale: {_display_scale}\ninit_image: {init_image}"""

        f = open(yaml, 'w')        
        f.write(yaml_settings)

    clear_output()
    txtC('>> Created YAML',f'yetiVideo={yetiVideo} > yetiMerge={yetiMerge}')
    txtC('>> Created Threshhold Masks',project)
    setupTime = timeTaken(start_time)
    # --------------------------------------------------------------------------
    return CONFIG_BASE_PATH, CONFIG_DEFAULTS, confPath, confPathIn, confPathOut, configPath, configPathIn, configPathOut, drivePath, drivePathIn, drivePathOut, driveOutProject, initVidPathIn, false, finalPathOut, finalList, finalStep, framesPathOut, imagesOut, initPathIn, initPathOut, init_file, init_image, init_name, localPath, localPathIn, localPathOut, maskPathOut, montFileFinal, montFileFrames, montFileMask, montPathOut, null, project, promptPathIn, settingsPathOut, stylePathIn, stylePathOut, threshMasked, timeSlug, true
    # --------------------------------------------------------------------------
    ############################################################################
    #END OF SCRIPT##############################################################
    ############################################################################
    ####################################################################yeti2022
    
    # if yetiMerge:
        #     finalList = os.listdir('/content/sample_data')
        #     finalListNum=len(finalList)
        #     mergeWeight=10/finalListNum
        #     mergeImages=f':{mergeWeight}\n | '.join(finalList)
        #     yaml_settingsMerge = f'''\
        #         file_namespace: {names}
        #         scene_prefix: ''
        #         scenes: ''
        #         width: {_width}
        #         cutouts: {_cut_outs}
        #         cut_pow: {_cut_pow}
        #         pixel_size: {_pixel_size}
        #         direct_init_weight: 10
        #         gradient_accumulation_steps: {_gradient_accumulation_steps}
        #         steps_per_scene: {_steps_per_scene}
        #         save_every: {_save_every}
        #         display_every: {_display_every}
        #         clear_every: {_clear_every}
        #         scene_suffix: {_scene_suffix}
        #         display_scale: {_display_scale}
        #         init_image: {init_image}
        #         direct_image_prompts: {mergeImages}
                
        #         '''
        #     f = open(yaml, 'w')
        #     f.write(yaml_settings)
