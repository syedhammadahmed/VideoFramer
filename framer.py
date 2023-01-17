import os
import random

import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
import myutil


# def framify(video_):
#     clip = cv2.VideoCapture(video_clip_name)
#     success, image = clip.read()
#     count = 0
#     while success:
#         x = '/home/syedhammadahmed/PycharmProjects/VideoTrimmer'
#         cv2.imwrite( x + "/WSAhvFpatFU/%d.jpg" % count, image)  # save frame as JPEG file
#         success, image = clip.read()
#         count += 1
#         print(str(count), " frames extracted from ", video_clip_path)


def framify(clip_name, clip_path, frames_root_path, clip_name):
    stream_type = "video"
    clip_file = clip_path + clip_name + myutil.get_stream_extension(stream_type)
    frame_root_dir = myutil.get_root_directory("frames") # /home/syedhammadahmed/Datasets/MOB/frames/
    stream_type = "video"
    video_class = "malign"
    frame_dir = frame_root_dir + stream_type + video_class + clip_name
    myutil.make_directory(frame_dir)
    clip = cv2.VideoCapture(clip_file)
    success, image = clip.read()
    count = 0
    while success:
        cv2.imwrite(frame_dir + str(count).zfill(4) + '.jpg', image)  # save frame as JPEG file
        success, image = clip.read()
        count += 1
        print(str(count), " frames extracted from ", video_clip_path)


if __name__ == '__main__':
    # framify('WSAhvFpatFU.mp4')
    n = 5
    file_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    sample = myutil.get_random_sublist(file_list, n)
    print(sample)
