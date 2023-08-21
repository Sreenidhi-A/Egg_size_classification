# -*- coding: utf-8 -*-
"""egg type classify .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W_R7kdYi-Xvyi1rs4hTpj1Mz5LkEZEqn
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')

import zipfile
zip_ref = zipfile.ZipFile('/content/kattu.zip', 'r')
zip_ref.extractall('/content')
zip_ref.close()

from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)

training_set = datagen.flow_from_directory(
        "/content/kattu/train",
        target_size=(64, 64),
        batch_size=32,
        class_mode="binary"
      )

datagen1 = ImageDataGenerator(rescale=1./255)

test_set = datagen1.flow_from_directory(
        "/content/kattu/test",
        target_size=(64, 64),
        batch_size=32,
        class_mode="binary"
      )

from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense

from tensorflow.keras.regularizers import l2

cnn = tf.keras.models.Sequential()

cnn.add(tf.keras.layers.Conv2D(filters=32,padding="same",kernel_size=3, activation='relu', strides=2, input_shape=[64, 64, 3]))

cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

cnn.add(tf.keras.layers.Conv2D(filters=32,padding='same',kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))

cnn.add(tf.keras.layers.Flatten())

cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))

cnn.add(Dense(1, kernel_regularizer=tf.keras.regularizers.l2(0.01),activation
             ='linear'))

cnn.summary()

cnn.compile(optimizer = 'adam', loss = 'hinge', metrics = ['accuracy'])

r=cnn.fit(x = training_set, validation_data = test_set, epochs = 15)

import matplotlib.pyplot as plt
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()

# plot the accuracy
plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.show()

from tensorflow.keras.preprocessing import image
import cv2
test_image = image.load_img('/content/8.jpg', target_size = (64,64))

plt.imshow(test_image)

test_image = image.img_to_array(test_image)
test_image=test_image/255
test_image = np.expand_dims(test_image, axis = 0)

result = cnn.predict(test_image)

if result[0]<0:
    print("The image classified is Ostrich egg")
else:
    print("The image classified is Normal egg ")

s=cnn.evaluate(test_set)

