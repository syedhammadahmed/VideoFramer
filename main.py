import logging
import os

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

import myutil
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Press the green button in the gutter to run the script.
def makeClips(video_id, video_class, stream_type):
    stream_type_index = myutil.clip_config["stream_type"].index(stream_type)
    video_extension = myutil.clip_config["stream_type_extension"][stream_type_index]
    video_name = video_id + "." + video_extension
    video_root_dir = myutil.get_download_root_directory()
    video_sub_dir = stream_type + "/" + video_class + "/" + video_name
    video_file_path = os.path.join(video_root_dir, video_sub_dir)
    clip_root_dir = myutil.get_clip_root_directory()
    clip_sub_dir = stream_type + "/" + video_class + "/" + video_id + "/"
    clip_file_path = os.path.join(clip_root_dir, clip_sub_dir)

    exists = os.path.exists(clip_file_path)
    if not exists:
        myutil.make_directory(clip_file_path)
        print(f"Directory '{clip_file_path}' created successfully...")

    if stream_type == "audio":
        clip = AudioFileClip(video_file_path)
    else:
        clip = VideoFileClip(video_file_path)
    clip_duration = myutil.clip_config["clip_duration"]

    clip_count = 0
    start_seconds = 0
    end_seconds = clip_duration
    video_duration = clip.duration - 1
    # print(video_duration)

    if video_duration < clip_duration:
        end_seconds = video_duration - 1

    myutil.add_log("video_id: " + str(video_id) + "\t|\t" + "duration: " + str(video_duration) + "\t|\t" + "video_path: " + video_file_path, logging.INFO)
    while end_seconds < video_duration:
        print(f"duration: {video_duration}, start: {start_seconds}, end: {end_seconds}");
        # problem when name contains '-'
        video_id = video_id.replace("-", "_")

        clip_name = clip_file_path + video_id + "_" + str(clip_count) + "." + video_extension
        clip_exists = os.path.exists(clip_name)
        if not clip_exists:
            # ffmpeg_extract_subclip(video_name, start_seconds, end_seconds, clip_name)
            sub_clip = clip.subclip(start_seconds, end_seconds)
            if stream_type == "audio":
                sub_clip.write_audiofile(clip_name)
            else:
                sub_clip.write_videofile(clip_name, fps=25)
        myutil.add_log("#" + str(clip_count) + ":" + "clip_name: " + clip_name + "\t|\t" + "[" + str(start_seconds) + "-" + str(end_seconds) + "]",
            logging.INFO)

        start_seconds += clip_duration
        end_seconds += clip_duration
        clip_count += 1

    return clip_count


if __name__ == '__main__':
    myutil.make_clip_directories()
    total_clips = 0
    total_videos = 0
    stream_type = "video"
    video_class = "malign"
    video_list = myutil.get_list_from_directory(myutil.get_dataset_file_directory() + stream_type + "/" + video_class + "/")
    for video_id in video_list:
        video_id = video_id[0:len(video_id)-4]
        total_videos += 1
        count = makeClips(video_id, video_class, stream_type)
        print(f"Total clips for video_id = {video_id} => {count}")
        total_clips += count
        # if total_videos == 5:
        #     break
    print(f"Total clips => {total_clips}")


