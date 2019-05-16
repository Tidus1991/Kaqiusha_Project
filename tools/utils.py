# -*- coding: utf-8 -*-
"""
Created on 2019/3/31 14:59

@author: Tidus
"""
import os
from scandir import scandir


image_extensions = [".jpg", ".jpeg", ".png"]

_video_extensions = [  # pylint: disable=invalid-name
    ".avi", ".flv", ".mkv", ".mov", ".mp4", ".mpeg", ".webm"]

class VideoRequire:
    def __init__(self, input_video):
        if input_video.split('.')[-1] not in _video_extensions:
            print('不支持该视频格式')

class Path_Manager:
    @staticmethod
    def ex_path(path):
        return os.path.exists(path)

    @staticmethod
    def is_path(path):
        return os.path.isdir(path)

    @staticmethod
    def make_path(path):
        os.mkdir(path)
        return

    @staticmethod
    def ch_path(path):
        os.chdir(path)
        return


def get_image_paths(directory):
    return [x.path for x in scandir(directory) if
     any(map(lambda ext: x.name.lower().endswith(ext), image_extensions))]

def queue_clear(state):
    while not state.empty():
        state.get()

def get_dir(dir_list, tar):
    target_video_filename = dir_list[0].split('/')[-1].split('.')[0]
    raw_video_filename = dir_list[1].split('/')[-1].split('.')[0]
    e_target_video_filename_path = target_video_filename  + '\\Extracted_image'
    e_raw_video_filename_path = raw_video_filename + '\\Extracted_image'
    model_dir = dir_list[2]
    output_dir = dir_list[3]
    if tar == 't':
        return 'ImageCache\\' + target_video_filename
    elif tar == 'r':
        return 'ImageCache\\' + raw_video_filename
    elif tar == 'e_t':
        return 'ImageCache\\' + e_target_video_filename_path
    elif tar == 'e_r':
        return 'ImageCache\\' + e_raw_video_filename_path
    elif tar == 'm':
        return model_dir + '_' + target_video_filename + '_' + raw_video_filename
    elif tar == 'o':
        return output_dir

