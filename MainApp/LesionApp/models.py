from django.db import models
from django.conf import settings
# from MainApp import settings
import matplotlib.image as mpimg
import tensorflow as tf
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
import skimage
from keras.models import load_model
import numpy as np
import os, cv2
from PIL import Image
import json
import efficientnet.tfkeras as efn


def make_padding(img):
    ht, wd, cc = img.shape
    ww = max(ht, wd)
    hh = max(ht, wd)
    color = (0, 0, 0)
    result = np.full((hh, ww, cc), color, dtype=np.uint8)
    xx = (ww - wd) // 2
    yy = (hh - ht) // 2
    # copy img image into center of result image
    result[yy:yy + ht, xx:xx + wd] = img

    return result

def crop_image(img, tol=60):
    mask = img > tol
    if img.ndim == 3:
        mask = mask.all(2)
    mask0, mask1 = mask.any(0), mask.any(1)

    return img[np.ix_(mask1, mask0)]

class Images(models.Model):

    image = models.ImageField(upload_to='images')
    gender = models.CharField(max_length=20)
    anatomic_site = models.CharField(max_length=50)
    group_age = models.CharField(max_length=6)
    result_binary = models.CharField(max_length=20, blank=True)
    result_multiclass = models.CharField(max_length=20, blank=True)
    pred_list = models.TextField(blank=True)


    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):

        im = mpimg.imread(self.image)
        img_extension = os.path.splitext(str(self.image))[1][1:]

        if img_extension == 'png':
            im *= 255
        if im.shape[0] != im.shape[1]:
            im = make_padding(im)
        im = crop_image(im)

        im = tf.dtypes.cast(im, tf.float32)
        im /= 255.0
        im = tf.image.resize_with_pad(im, 224, 224)
        im = np.expand_dims(im, axis=0)

        try:
            file_model = os.path.join(settings.BASE_DIR, 'WBT_Multi.h5')
            graph = tf.compat.v1.get_default_graph()

            with graph.as_default():

                print('HERE' * 100)
                my_model = tf.keras.models.load_model(file_model)
                best_checkpoint = os.path.join(settings.BASE_DIR, 'cp-72.ckpt')
                my_model.load_weights(best_checkpoint)
                print(my_model)

                Y_pred = my_model.predict(im)
                print('HERE' * 100)
                y_pred = Y_pred.argmax(axis=1)
                label = ['Actinic keratosis (AK)', 'Basal cell carcinoma (BCC)',
                         'Benign keratosis (BKL)', 'Dermatofibroma (DF)', 'Melanoma (MEL)',
                         'Melanocytic nevus (NV)', 'Squamous cell carcinoma (SCC)',
                         'unknown (UNK)', 'Vascular (VASC)']
                self.result_multiclass = label[int(y_pred)]
                Y_pred = Y_pred.tolist()
                self.pred_list = json.dumps(Y_pred)
                # Set binary classification
                benign_list = [2, 3, 5]
                malignant_list = [1, 4, 6]
                danger_list = [0, 8]
                if y_pred in benign_list:
                    self.result_binary = 'benign'
                elif y_pred in malignant_list:
                    self.result_binary = 'malignant'
                elif y_pred in danger_list:
                    self.result_binary = 'not malignant not benign'
                else:
                    self.result_binary = 'unknown'

                print(y_pred)
                print(Y_pred)
        except:
            self.result_multiclass = 'failed to classify'

        return super().save(*args, **kwargs)

