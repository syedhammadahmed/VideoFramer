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


def framify(clip_name, clip_path, frames_root_path):
    stream_type = "video"
    video_class = "malign"
    clip_file = clip_path + stream_type + '/' + video_class + '/' + clip_name + '.' + myutil.get_stream_extension(stream_type)
    frame_dir = frames_root_path + stream_type + '/' + video_class + '/' + clip_name + '/'
    exists = myutil.make_directory(frame_dir)
    if exists:
        print('frames directory', frame_dir, 'exists')

    clip = cv2.VideoCapture(clip_file)
    success, image = clip.read()
    count = 0
    while success:
        new_frame_file = frame_dir + str(count).zfill(4) + '.jpg'
        exists = os.path.exists(new_frame_file)
        if not exists:
            cv2.imwrite(new_frame_file, image)  # save frame as JPEG file
            success, image = clip.read()
            count += 1
    print(str(count), " frames extracted from the clip: ", clip_name)
    return count

if __name__ == '__main__':
    frames_root_path = myutil.get_root_directory("frames") # /home/syedhammadahmed/Datasets/MOB/frames/
    clips_root_path = myutil.get_root_directory("clips") # /home/syedhammadahmed/Datasets/MOB/clips/
    # framify('WSAhvFpatFU.mp4')
    total_frames = 0
    total_videos = 0
    stream_type = "video"
    video_class = "malign"
    clip_list = myutil.get_list_from_directory(myutil.get_root_directory("clips") + stream_type + "/" + video_class + "/")
    for clip_name in clip_list:
        clip_name = clip_name[0:len(clip_name)-4]
        count = framify(clip_name, clips_root_path, frames_root_path)
        total_videos += 1
        total_frames += count
        if total_videos == 5:
            break
    print(f"Total frames => {total_frames}")





    # n = 5
    # file_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    # sample = myutil.get_random_sublist(file_list, n)
    # print(sample)
