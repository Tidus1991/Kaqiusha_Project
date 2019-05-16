# -*- coding: utf-8 -*-
"""
Created on 2019/4/9 16:22

@author: Tidus
"""

from tools.utils import get_image_paths, queue_clear, get_dir
import cv2
from tqdm import tqdm
import os

class MergeImage:
    #t ASK, r me
    def __init__(self, dir_list, state = None, fps = 30):
        self.state = state
        self.output_path = dir_list[3]
        self.img_path = get_dir(dir_list, 't')
        self.raw_path = get_dir(dir_list, 'r')
        self.exit_flag = False
        self.fps = fps
        try :
            if self.state is not None:
                if not self.state.empty():
                    if self.state.get() == 'stop_con':
                        self.exit_flag = True
                        print('取消合成，正在清理缓存文件。')
                        return
            self.process()
        finally:
            if not self.exit_flag:
                print('合成完成')
            elif self.exit_flag:
                path = self.img_path + '_convert'
                if os.path.exists(path):
                    import shutil
                    shutil.rmtree(path)

    def process(self):
        img_list = get_image_paths(self.img_path)
        temp = cv2.imread(img_list[0])
        height, width, layers = temp.shape;  size = (width,height)
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        video_writer = cv2.VideoWriter(self.output_path + '\\' + self.img_path
                                       + '.avi', fourcc, self.fps, size)
        for i in tqdm(range(len(img_list))):
            if self.state is not None:
                if not self.state.empty():
                    if self.state.get() == 'stop_con':
                        self.exit_flag = True
                        print('取消合成，正在清理缓存文件。')
                        break
            frame = cv2.imread(self.img_path + '\\' + str(i) + '.jpg')
            video_writer.write(frame)
        video_writer.release()
        queue_clear(self.state)