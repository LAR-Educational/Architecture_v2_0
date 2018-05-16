from mobilenet import generate_mobilenet
import os
import numpy as np
import cv2
import vars

labels_dict = vars.labels_dict
input_shape = vars.input_shape

class Classifier:
    def __init__(self, classifier="sf_model"):
        self.classifier = classifier
        self.emotion
        self.model_a
        self.model_b

        if self.classifier == "single_model":
            self.model_a = generate_mobilenet(input_shape, 7)
            self.model_a.load_weights('models/mobilenet-monster-noweight.h5')

        if self.classifier == "ff_model":
            self.model_a = generate_mobilenet(input_shape, 4)
            self.model_a.load_weights('models/mobilenet-monster-first.h5')
            self.model_b = generate_mobilenet(input_shape, 4)
            self.model_b.load_weights('models/mobilenet-monster-second.h5')

        if self.classifier == "sf_model":
            self.model_a = generate_mobilenet(input_shape, 7)
            self.model_a.load_weights('models/mobilenet-monster-noweight.h5')
            self.model_b = generate_mobilenet(input_shape, 4)
            self.model_b.load_weights('models/mobilenet-monster-second.h5')

    def inference(self, image):
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
