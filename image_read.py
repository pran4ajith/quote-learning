from google.cloud import vision
from google.cloud.vision import types
import io, os
from collections import OrderedDict 
from nltk.tokenize import word_tokenize

import re

'''
This module is an interface to the google vision API output.
Returns the labels for the uploaded image.
'''

def im_read(path):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.abspath(path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    # Performs label detection on the image file
    label_response = client.label_detection(image=image)

    landmark_response = client.landmark_detection(image=image)
    labels = read_labels(label_response)
    landmarks = read_landmark(landmark_response)
    if(landmarks):
        return pre_process(landmarks)
    else:
        return pre_process(labels)
# image_desc  = ' '.join(image_data[image_data['score']>0.8]['description'].to_list())

def pre_process(text):
    text = " ".join(text)
    # misattributed, attributed checks is specific to the dataset I used
    text = re.sub(r'[^A-Za-z-\n ]|(misattributed\S+)|(from\S+)|(attributed\S+)', '', text.lower().strip())
    text = re.sub(r'[-]', ' ', text)

    text = word_tokenize(text)
    return text

def read_labels(response):
    labels = response.label_annotations
    labels = [label.description for label in labels if(label.score>0.0)]
    # print(labels)
    return list(OrderedDict.fromkeys(labels)) 


def read_landmark(response): 
    landmarks = response.landmark_annotations

    landmarks = [landmark.description for landmark in landmarks]
    # print(landmarks)

    if response.error.message:
        raise Exception(response.error.message)
    return list(OrderedDict.fromkeys(landmarks)) 
