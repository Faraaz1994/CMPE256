from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras.models import load_model
from keras.utils import to_categorical
from keras.utils import to_categorical
from numpy import asarray
import numpy as np

from keras.models import Sequential
from keras.constraints import maxnorm
from keras.optimizers import SGD

from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

def trainModel():
  return createModel(64,64,1,62,'model_weights.hdf5')

def createModel(img_width,img_height,channels,num_classes,filePath):
  model = Sequential()
  model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, channels), padding='same', activation='relu', kernel_constraint=maxnorm(3)))
  model.add(Dropout(0.2))
  model.add(Conv2D(32, (3, 3), activation='relu', padding='same', kernel_constraint=maxnorm(3)))
  model.add(MaxPooling2D())
  model.add(Flatten())
  model.add(Dense(512, activation='relu', kernel_constraint=maxnorm(3)))
  model.add(Dropout(0.5))
  model.add(Dense(num_classes, activation='softmax'))
  lrate=0.01
  epochs = 100
  decay = lrate/epochs
  sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
  model.load_weights(filePath)
  model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
  return model 
  