import os

import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
import myutil

frame_config = {
    "win_root": "E:",
    "linux_root": os.path.expanduser('~'),
    "clips_directory": "/Datasets/MOB/clips/",
    "frames_directory": "/Datasets/MOB/frames/",
    "dataset_file": "dataset.xlsx",
    "clip_duration": 10, # in seconds
    "classes": ["benign", "malign"],
    "stream_type": ["audio", "video"],
    "stream_type_extension": ["m4a", "mp4"],
    "clip_api_class": ["moviepy.audio.io.AudioFileClip", "moviepy.video.io.VideoFileClip"],
    "log_directory": "logs/"
}

def framify(video_clip_name):
    clip = cv2.VideoCapture(video_clip_name)
    success, image = clip.read()
    count = 0
    while success:
        x = '/home/syedhammadahmed/PycharmProjects/VideoTrimmer'
        cv2.imwrite( x + "/WSAhvFpatFU/%d.jpg" % count, image)  # save frame as JPEG file
        success, image = clip.read()
        count += 1
        print(str(count), " frames extracted from ", video_clip_path)



if __name__ == '__main__':
    framify('WSAhvFpatFU.mp4')