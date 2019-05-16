# -*- coding: utf-8 -*-
"""
Created on 2019/3/31 16:58

@author: Tidus
"""
import cv2
from tools.utils import Path_Manager, get_dir
import os

class Video2Figure:
    def __init__(self, dir_list, state):
        try:
            os.mkdir('ImageCache')
        except:
            import shutil
            shutil.rmtree('ImageCache')
            os.mkdir('ImageCache')

        self.exit_flag = False
        self.state = state
        if not self.state.empty():
            if self.state.get() == 'stop_pre':
                self.exit_flag = True
        for temp in ['t','r']:
            if self.exit_flag:
                break
            if temp == 't':
                print('-----------------开始提取目标视频帧------------------')
            else:
                print('-----------------开始提取素材视频帧------------------')
            self.input_video_name = get_dir(dir_list, temp)
            if temp == 't':
                self.v2f(dir_list[0])
            elif temp == 'r':
                self.v2f(dir_list[1])

    def v2f(self, input_video_path_name):
        if not os.path.exists(self.input_video_name.split('\\')[-1]):
            os.mkdir(self.input_video_name)
        else:
            import shutil
            shutil.rmtree('ImageCache')
            os.mkdir('ImageCache')
        cap = cv2.VideoCapture(input_video_path_name)
        index = 0
        while (cap.isOpened()):
            if not self.state.empty():
                if self.state.get() == 'stop_pre':
                    self.exit_flag = True
                    break
            index += 1
            ret, frame = cap.read()
            if index % 50 == 49:
                print('视频抽取已完成%i帧'%(index + 1), flush = False)
            if frame is None:
                break
            cv2.imwrite(self.input_video_name + '\%s'%(str(index)) + '.jpg', frame)
        cap.release()
        cv2.destroyAllWindows()
        print('--------------------帧提取结束----------------------')
