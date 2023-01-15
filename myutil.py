import os
from datetime import datetime
from os import listdir
from os.path import isfile, join
from os import listdir
from sys import platform
import pandas as pd
import logging

clip_config = {
    "win_root": "D:",
    "linux_root": os.path.expanduser('~'),
    "videos_directory": "/Datasets/MOB/",
    "clips_directory": "/Datasets/MOB/clips/",
    "dataset_file": "dataset.xlsx",
    "clip_duration": 10, # in seconds
    "classes": ["benign", "malign"],
    "stream_type": ["audio", "video"],
    "stream_type_extension": ["m4a", "mp4"],
    "clip_api_class": ["moviepy.audio.io.AudioFileClip", "moviepy.video.io.VideoFileClip"],
    "log_directory": "logs/"
}


def get_clip_root_directory():
    if platform == "linux" or platform == "linux2":
        return clip_config["linux_root"] + clip_config["clips_directory"]
    elif platform == "win32":
        return clip_config["win_root"] + clip_config["clips_directory"]

def get_download_root_directory():
    if platform == "linux" or platform == "linux2":
        return clip_config["linux_root"] + clip_config["videos_directory"]
    elif platform == "win32":
        return clip_config["win_root"] + clip_config["videos_directory"]

def get_dataset_file_directory():
    if platform == "linux" or platform == "linux2":
        return clip_config["linux_root"] + clip_config["videos_directory"]
    elif platform == "win32":
        return clip_config["win_root"] + clip_config["videos_directory"]


def make_directory(path):
    try:
        # os.mkdir(path)
        exists = os.path.exists(path)
        os.makedirs(path, 0o777, exist_ok="True")
    except OSError as error:
        print(error)
    return exists

def get_list_from_excel(dataset_filename, video_class):
    sheet_df = pd.read_excel(dataset_filename, sheet_name=video_class)
    sheet_np = sheet_df.to_numpy()
    video_list = sheet_np[:, 0]
    return video_list

def make_clip_directories():
    root_dir = get_clip_root_directory()
    stream_type = "video"
    video_class = "malign"
    # video_list = get_list_from_excel(get_dataset_file_directory() + clip_config["dataset_file"], video_class)
    video_list = get_list_from_directory(get_dataset_file_directory() + stream_type + "/" + video_class + "/")
    for video_id in video_list:
        video_id = video_id[0:len(video_id)-4]
        sub_dir = stream_type + "/" + video_class + "/" + video_id + "/"
        download_file_path = os.path.join(root_dir, sub_dir)
        exists = make_directory(download_file_path)
        if not exists:
            print(f"Directory '{download_file_path}' created successfully...")
        else:
            print(f"Directory '{download_file_path}' already exists...")


def get_list_from_directory(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files

def get_log_directory():
    return get_clip_root_directory() + clip_config["log_directory"]

def add_log(msg, level):
    log_file = datetime.now().strftime("%m%d%Y%H%M") + ".log"
    # if not os.path.exists(log_file):
    #     f = open(log_file, "w")
    log_directory = get_log_directory()
    make_directory(log_directory)
    logging.basicConfig(filename=log_directory + log_file,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    logger = logging.getLogger('MOB_CLIPPER')
    logger.log(level, msg)
