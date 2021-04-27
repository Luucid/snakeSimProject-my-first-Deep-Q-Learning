import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import time
from GameClass import trainPack


model = keras.Sequential([
    keras.layers.Flatten(input_shape=(4, 4)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(16, activation='softmax')])

model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])


model.fit(trainPack, epochs=12)