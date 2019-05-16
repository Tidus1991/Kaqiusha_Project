# -*- coding: utf-8 -*-
"""
Created on 2019/4/1 21:09

@author: Tidus
"""
from tools.utils import get_image_paths, get_dir
import keras
from plugins import Model_Original
import threading

class TrainingProcessor(object):
    def __init__(self, dir_list, state = None):
        self.input_A_path = get_dir(dir_list, 't')
        self.input_B_path = get_dir(dir_list, 'r')
        self.model_path = get_dir(dir_list, 'm')
        self.state = state
        self.GPU_check()
        keras.backend.clear_session()
        self.process()

    def process(self):

        self.save_now = True
        thr = threading.Thread(target=self.processThread, args=(), kwargs={})
        # input() # TODO how to catch a specific key instead of Enter?
        thr.start()
        self.stop = False
        self.exit_flag = False
        thr.join()

    def GPU_check(self):
        GPU_list = keras.backend.tensorflow_backend._get_available_gpus()
        if GPU_list:
            GPU_num = len(GPU_list)
            print('\n###识别出%d个可使用的GPU，分别为\n###%s\n###'%(GPU_num, ('\n'+','.join(GPU_list))))
        else:
            print('\n###未识别出可使用的GPU，将会使用CPU进行训练程序，这会可能极大地影响训练效率###\n')

    def processThread(self):
        print('正在载入训练数据……………………')
        trainer = 'Original'
        # model = PluginLoader.get_model(trainer)(self.model_path)
        model = Model_Original.Model(self.model_path)
        model.load(swapped = False)
        images_A = get_image_paths(self.input_A_path + '\\' + 'Extracted_image')
        images_B = get_image_paths(self.input_B_path + '\\' + 'Extracted_image')
        trainer = Model_Original.Trainer(model,
                                                    images_A,
                                                    images_B,
                                                    batch_size=64)

        # trainer = PluginLoader.get_trainer(trainer)(model,
        #                                             images_A,
        #                                             images_B,
        #                                             batch_size=64)

        try:
            print('--------------------开始训练模型--------------------')
            # os.mkdir('fuck5')
            for epoch in range(0, 10000):
                # save_iteration = epoch % self.arguments.save_interval == 0

                # trainer.train_one_step(epoch, self.show if (save_iteration or self.save_now) else None)

                # if save_iteration:
                #     model.save_weights()
                loss_A, loss_B = trainer.train_one_step(epoch, None)

                if self.stop:
                    model.save_weights()
                    exit()

                if not self.state.empty():
                    if self.state.get() == 'stop_tra':
                        self.exit_flag = True
                        exit()
                #
                if epoch % 50 == 5:
                    model.save_weights()

                if (loss_A < 0.1 or loss_B < 0.1) and epoch >= 5:
                    model.save_weights()
                    break

        except KeyboardInterrupt:
            model.save_weights()
            exit(0)

        finally:
            model.save_weights()
            keras.backend.clear_session()
            print('--------------------模型训练已停止-------------------')
