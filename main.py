from GameClass import Game
import tensorflow as tf
import tensorflow.keras as keras
from time import sleep
from GameClass import trainPack


matches = 10
for i in range(matches):
    game = Game()
    game.startGame()
    




model = keras.Sequential([
    keras.layers.Flatten(input_shape=(4, 4)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(16, activation='softmax')])

model.compile(optimizer = 'adam',
              loss = 'sparse_categorical_crossentropy',
              metrics = ['accuracy'])


model.fit(trainPack, epochs=12)