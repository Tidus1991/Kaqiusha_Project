# -*- coding: utf-8 -*-
"""
Created on 2019/3/31 15:23

@author: Tidus
"""

import os
import cv2
from tools.utils import Path_Manager, queue_clear, get_dir
from lib.cli import DirectoryProcessor
from plugins import Extract_Align

class ExtractTrainingData(DirectoryProcessor):
    def process(self, state):
        self.exit_flag = False
        self.state = state
        if not self.state.empty():
            if self.state.get() == 'stop_pre':
                self.exit_flag = True
        extractor = Extract_Align.Extract()
        for temp in ['t','r']:
            if self.exit_flag:
                break
            if temp == 't':
                print('---------------开始提取目标视频面部区域---------------')
            else:
                print('---------------开始提取素材视频面部区域---------------')

            output_image_filename = get_dir(self.dir_list, temp)
            filenames = os.listdir(output_image_filename)
            Path_Manager.make_path(output_image_filename+'\\Extracted_image')
            index = 0
            for filename in filenames:
                if self.exit_flag:
                    break
                if not self.state.empty():
                    if self.state.get() == 'stop_pre':
                        self.exit_flag = True
                if filename == 'Extracted_image':
                    continue
                index += 1
                image = cv2.imread(output_image_filename + '\\' + filename)

                for idx, face in self.get_faces(image):
                    if index %50 == 49:
                        print('面部提取已完成%i帧'%(index + 1))
                    resized_image = extractor.extract(image, face, 256)
                    cv2.imwrite(output_image_filename + '\\Extracted_image\\' + 'Extracted_image_' + str(index) + '.jpg',
                                resized_image)
        queue_clear(self.state)
        print('-------------------面部区域提取结束------------------')