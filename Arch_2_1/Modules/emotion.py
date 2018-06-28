from Emotion import mobilenet
import os
import numpy as np
import cv2
from vars import info, war, error

labels_dict = {
	0: 'happy', 1: 'neutral', 2: 'surprise',
	3: 'fear', 4: 'disgust', 5: 'angry', 6: 'sad'}
input_shape = (224,224,3)


class Classifier:
    def __init__(self, classifier="sf_model"):
        self.classifier = classifier
        self.model_a = ""
        self.model_b = ""

        info("Initializing classifier with " + self.classifier)
        if self.classifier == "single_model":
            self.model_a = mobilenet.generate_mobilenet(input_shape, 7)
            self.model_a.load_weights('Modules/Emotion/models/mobilenet-monster-noweight.h5')

        if self.classifier == "ff_model":
            self.model_a = mobilenet.generate_mobilenet(input_shape, 4)
            self.model_a.load_weights('Modules/Emotion/models/mobilenet-monster-first.h5')
            self.model_b = mobilenet.generate_mobilenet(input_shape, 4)
            self.model_b.load_weights('Modules/Emotion/models/mobilenet-monster-second.h5')

        if self.classifier == "sf_model":
            self.model_a = mobilenet.generate_mobilenet(input_shape, 7)
            self.model_a.load_weights('Modules/Emotion/models/mobilenet-monster-noweight.h5')
            self.model_b = mobilenet.generate_mobilenet(input_shape, 4)
            self.model_b.load_weights('Modules/Emotion/models/mobilenet-monster-second.h5')

        info("Weights loaded. Model initialized!")
    
    def inference(self, image):
        info("Making inference on image...")
        if self.classifier == "single_model":
            result = self.model_a.predict(np.expand_dims(image, axis=0), batch_size=1, verbose=0)
            return labels_dict[np.argmax(result[0])]
        elif self.classifier == "ff_model":
            result = self.model_a.predict(np.expand_dims(image, axis=0), batch_size=1, verbose=0)
            pred = np.argmax(result[0])
            if pred == 1:
                r = self.model_b.predict(np.expand_dims(image, axis=0), batch_size=1, verbose=0)
                pred = np.argmax(r[0]) + 3
            elif pred != 0:
                pred -= 1
            return labels_dict[pred]
        elif self.classifier == "sf_model":
            result = self.model_a.predict(np.expand_dims(image, axis=0), batch_size=1, verbose=0)
            pred = np.argmax(result[0])
            if pred in [3,4,5,6]:
                r = self.model_b.predict(np.expand_dims(image, axis=0), batch_size=1, verbose=0)
                pred = np.argmax(r[0]) + 3
            return labels_dict[pred]
