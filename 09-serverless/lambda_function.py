#!/usr/bin/env python
# coding: utf-8

from io import BytesIO
from urllib import request
from PIL import Image
import numpy as np
import tflite_runtime.interpreter as tflite


def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def predict(url):
    img = download_image(url)
    img = prepare_image(img, (150, 150))
    x = np.array(img)
    X = np.array([x])
    X = X / 255.0
    X = X.astype('float32')

    interpreter = tflite.Interpreter(model_path='bees-wasps-v2.tflite')
    interpreter.allocate_tensors()

    input_index = interpreter.get_input_details()[0]['index']
    output_index= interpreter.get_output_details()[0]['index']

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    return interpreter.get_tensor(output_index)


def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    result = result[0].tolist()
    return result