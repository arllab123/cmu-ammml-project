# coding=utf-8
# vgg16.py: VGGNet implementation by Lorenzo Baraldi.
# https://gist.github.com/baraldilorenzo/07d7802847aaad0a35d3

from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Convolution2D, MaxPooling2D,\
    ZeroPadding2D


def VGG16(weights_path=None, default_arch_weights=True):
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(224,224,3)))
    model.add(Convolution2D(64, 3, 3, activation="relu",trainable=False))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation="relu",trainable=False))
    model.add(MaxPooling2D((2,2), strides=(2,2),dim_ordering="tf"))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, 3, 3, activation="relu",trainable=False))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, 3, 3, activation="relu",trainable=False))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation="relu",trainable=False))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation="relu",trainable=False))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation="relu",trainable=False))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation="relu"))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation="relu"))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation="relu"))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation="relu"))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation="relu"))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation="relu"))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(Flatten())
    model.add(Dense(4096, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(1000, activation="softmax"))

    if weights_path is not None and default_arch_weights is True:
        model.load_weights(weights_path)

    model.layers.pop()
    model.add(Dense(1, activation="sigmoid"))

    if weights_path is not None and default_arch_weights is False:
        model.load_weights(weights_path)

    # HACK LEVEL: OVER 9000!!!
    layers = []
    for i in range(len(model.layers)):
        layers.append(model.layers[i])
        print(model.layers[i])
    model2 = Sequential()
    part_lens = [17, 14]
    layer_idx = 0
    for part_len in part_lens:
        for _ in range(part_len):
            model2.add(layers[layer_idx])
            layer_idx += 1
        model2.add(Dropout(0.5))
    while layer_idx < len(layers):
        model2.add(layers[layer_idx])
        layer_idx += 1 

    return model2

