# AutoEncoder base classes

import numpy
from lib.training_data import minibatchAB, stack_images
import os

encoderH5 = '/encoder.h5'
decoder_AH5 = '/decoder_A.h5'
decoder_BH5 = '/decoder_B.h5'

class ModelAE:
    def __init__(self, model_dir):

        self.model_dir = model_dir

        self.encoder = self.Encoder()
        self.decoder_A = self.Decoder()
        self.decoder_B = self.Decoder()

        self.initModel()

    def load(self, swapped):
        (face_A,face_B) = (decoder_AH5, decoder_BH5) if not swapped else (decoder_BH5, decoder_AH5)
        if not os.path.exists(self.model_dir):
            os.mkdir(self.model_dir)
            print('没有找到目标视频的训练模型，正在新建训练模型文件')
        try:
            self.save_weights()
        except:
            print('训练模型读取失败，请重新尝试')
            import shutil
            shutil.rmtree(self.model_dir)
            exit(1)

        self.encoder.load_weights(self.model_dir + encoderH5)
        self.decoder_A.load_weights(self.model_dir + face_A)
        self.decoder_B.load_weights(self.model_dir + face_B)
        print('正在读取训练模型……………………')
        return True

    def save_weights(self):
        self.encoder.save_weights(self.model_dir + encoderH5)
        self.decoder_A.save_weights(self.model_dir + decoder_AH5)
        self.decoder_B.save_weights(self.model_dir + decoder_BH5)
        print('训练模型已自动保存')

class TrainerAE():
    def __init__(self, model, fn_A, fn_B, batch_size=64):
        self.batch_size = batch_size
        self.model = model
        self.images_A = minibatchAB(fn_A, self.batch_size)
        self.images_B = minibatchAB(fn_B, self.batch_size)

    def train_one_step(self, iter, viewer):
        epoch, warped_A, target_A = next(self.images_A)
        epoch, warped_B, target_B = next(self.images_B)
        loss_A = self.model.autoencoder_A.train_on_batch(warped_A, target_A)
        loss_B = self.model.autoencoder_B.train_on_batch(warped_B, target_B)
        print("epoch: %i     loss_A: %f     loss_B: %f"%((iter + 1), loss_A, loss_B))

        if viewer is not None:
            viewer(self.show_sample(target_A[0:14], target_B[0:14]), "training")
        return loss_A,loss_B

    def show_sample(self, test_A, test_B):
        figure_A = numpy.stack([
            test_A,
            self.model.autoencoder_A.predict(test_A),
            self.model.autoencoder_B.predict(test_A),
        ], axis=1)
        figure_B = numpy.stack([
            test_B,
            self.model.autoencoder_B.predict(test_B),
            self.model.autoencoder_A.predict(test_B),
        ], axis=1)

        figure = numpy.concatenate([figure_A, figure_B], axis=0)
        figure = figure.reshape((4, 7) + figure.shape[1:])
        figure = stack_images(figure)

        return numpy.clip(figure * 255, 0, 255).astype('uint8')
