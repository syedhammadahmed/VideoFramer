import os
import random
from datetime import datetime
from os import listdir
from os.path import isfile, join
from os import listdir
from sys import platform
import pandas as pd
import logging

frame_config = {
    "win_root": "E:",
    "linux_root": os.path.expanduser('~'),
    "dataset_root": "/Datasets/MOB/",
    "clips_sub_root": "clips/",
    "frames_sub_root": "frames/",
    "dataset_file": "clips.xlsx",
    "classes": ["benign", "malign"],
    "stream_type": ["audio", "video"],
    "stream_type_extension": ["m4a", "mp4"],
    "log_directory": "logs/"
}

def get_stream_extension(stream_type):
    stream_type_index = frame_config["stream_type"].index(stream_type)
    extension = frame_config["stream_type_extension"][stream_type_index]
    return extension


# options: 'clips', 'frames'
def get_root_directory(name='clips'): #e.g. for the key 'clips_directory'
    os_root = frame_config["linux_root"]
    # if platform == "linux" or platform == "linux2":
    if platform == "win32":
        os_root = frame_config["win_root"]

    return os_root + frame_config["dataset_root"] + frame_config[name + "_sub_root"]


def get_dataset_file():
    if platform == "linux" or platform == "linux2":
        return frame_config["linux_root"] + frame_config["clips_directory"] + frame_config["dataset_file"]
    elif platform == "win32":
        return frame_config["win_root"] + frame_config["clips_directory"] + frame_config["dataset_file"]


def make_directory(path):
    try:
        exists = os.path.exists(path)
        os.makedirs(path, 0o777, exist_ok="True")
    except OSError as error:
        print(error)
    return exists


#returns all elements in the first column by default
def get_list_from_excel(file_name, sheet_name, row_start=0, row_end=-1, column_start=0, column_end=1):
    sheet_df = pd.read_excel(file_name, sheet_name=sheet_name)
    sheet_np = sheet_df.to_numpy()
    video_list = sheet_np[row_start:row_end, column_start:column_end]
    return video_list


def make_frame_directories():
    clip_root_dir = get_clip_root_directory()
    frame_root_dir = get_frame_root_directory()
    stream_type = "video"
    video_class = "malign"
    # video_list = get_list_from_excel(get_dataset_file_directory() + frame_config["dataset_file"], video_class)
    video_list = get_list_from_directory(root_dir + stream_type + "/" + video_class + "/", False)
    for video_id in video_list:
        video_id = video_id[0:len(video_id) - 4]
        sub_dir = stream_type + "/" + video_class + "/" + video_id + "/"
        download_file_path = os.path.join(root_dir, sub_dir)
        exists = make_directory(download_file_path)
        if not exists:
            print(f"Directory '{download_file_path}' created successfully...")
        else:
            print(f"Directory '{download_file_path}' already exists...")


def get_list_from_directory(path, is_file=True):
    if not is_file:
        files = [f for f in listdir(path) if not isfile(join(path, f))]
    else:
        files = [f for f in listdir(path) if isfile(join(path, f))]
    return files


def get_log_directory():
    return get_clip_root_directory() + frame_config["log_directory"]


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


# print(get_list_from_excel(get_dataset_file(), "malign"))
# make_frame_directories()