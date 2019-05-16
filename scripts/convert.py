# -*- coding: utf-8 -*-
"""
Created on 2019/4/8 14:44

@author: Tidus
"""

import cv2
import re, os
import keras
from lib.cli import DirectoryProcessor
from lib.utils import BackgroundGenerator
from plugins import Model_Original, Convert_Masked

class ConvertImage(DirectoryProcessor):
    filename = ''
    def process(self):
        self.convert_cache = self.input_A_path + '_convert'
        try:
            os.mkdir(self.convert_cache)
        except:
            import shutil
            shutil.rmtree(self.convert_cache)
            os.mkdir(self.convert_cache)

        # model_name = 'Original'
        # conv_name = 'Masked' #'Masked'
        # model = PluginLoader.get_model(model_name)(self.model_path)
        model = Model_Original.Model(self.model_path)

        if not model.load(swapped = True):
            exit(1)

        converter = Convert_Masked.Convert(model.converter(False),
                              blur_size=2,
                              seamless_clone=True,
                              mask_type="facehullandrect",
                              erosion_kernel_size=None,
                              smooth_mask=True,
                              avg_color_adjust=True
                                                          )

        batch = BackgroundGenerator(self.prepare_images(), 1)

        self.frame_ranges = None
        minmax = {
            "min": 0, # never any frames less than 0
            "max": float("inf")
        }
        if self.frame_ranges:
            self.frame_ranges = [tuple(map(lambda q: minmax[q] if q in minmax.keys() else int(q), v.split("-"))) for v in self.arguments.frame_ranges]
        self.imageidxre = re.compile(r'(\d+)(?!.*\d)')
        try:
            for item in batch.iterator():
                if not self.state.empty():
                    if self.state.get() == 'stop_con':
                        print('取消合成，正在清理缓存文件')
                        break
                    else:
                        self.convert(converter, item)
                else:
                    self.convert(converter, item)
        finally:
            keras.backend.clear_session()

    def convert(self, converter, item):
        # try:
        (filename, image, faces) = item

        skip = self.check_skip(filename)

        # if not skip:  # process as normal
        for idx, face in faces:
            image = converter.patch_image(image, face)
        # output_file = os.getcwd()

        # if self.arguments.discard_frames and skip:
        #     return
        cv2.imwrite(self.convert_cache + '\\' + str(filename).split('\\')[-1], image)
        # except Exception as e:
        #     print('Failed to convert image: {}. Reason: {}'.format(filename, e))

    def check_skip(self, filename):
        try:
            idx = int(self.imageidxre.findall(filename)[0])
            return not any(map(lambda b: b[0] <= idx <= b[1], self.frame_ranges))
        except:
            return False

    def prepare_images(self):
        for filename in self.read_directory():
            image = cv2.imread(filename)
            yield filename, image, self.get_faces(image)

