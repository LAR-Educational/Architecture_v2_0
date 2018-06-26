from mobilenet import generate_mobilenet
import os
import numpy as np
import cv2


labels_dict = {
    0: 'happy', 1: 'neutral', 2: 'surprise',
    3: 'fear', 4: 'disgust', 5: 'angry', 6: 'sad'}

def single_model_inf(model, image):
    result = model.predict(np.expand_dims(image, axis=0),
                           batch_size=1, verbose=0)
    return labels_dict[np.argmax(result[0])]

def ff_model_inf(model_a, model_b, image):
    '''
    4-4 model inference
    '''
    result = model_a.predict(np.expand_dims(image, axis=0),
                             batch_size=1, verbose=0)
    pred = np.argmax(result[0])
    if pred == 1:
        r = model_b.predict(np.expand_dims(image, axis=0),
                            batch_size=1, verbose=0)
        pred = np.argmax(r[0]) + 3
    elif pred != 0:
        pred -= 1
    return labels_dict[pred]


def sf_model_inf(model_a, model_b, image):
    '''
    7-4 model inference
    '''
    result = model_a.predict(np.expand_dims(image, axis=0),
                             batch_size=1, verbose=0)
    pred = np.argmax(result[0])
    if pred in [3,4,5,6]:
        r = model_b.predict(np.expand_dims(image, axis=0),
                            batch_size=1, verbose=0)
        pred = np.argmax(r[0]) + 3
    return labels_dict[pred]



input_shape = (224,224,3)

# generating model and loading weights
mobilenet_s = generate_mobilenet(input_shape, 7)
mobilenet_s.load_weights('models/mobilenet-monster-noweight.h5')

# mobilenet_sup = generate_mobilenet(input_shape, 4)
# mobilenet_sup.load_weights('models/mobilenet-monster-first.h5')
#
# mobilenet_neg = generate_mobilenet(input_shape, 4)
# mobilenet_neg.load_weights('models/mobilenet-monster-second.h5')

#for i in os.listdir('sample'):

cap = cv2.VideoCapture(0)

flag=True

while flag:
    # reading grayscale png (with 3 channels)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        # cv2.imshow('frame',gray)
        key = cv2.waitKey(1)
        #print key
        if key == 1048689: #ord('q'):
            break
        
        if key == 1048695: #ord('w'):
            flag=False
            break
        
    
        vec = np.stack([gray,gray,gray], axis=2)
        print(vec.shape)

    
        #exit()
    
    
        image = vec #gray #cv2.imread('sample/{}'.format(i))
        r_image = cv2.resize(image, input_shape[:2])*1./255

        # 7
        emotion_s = single_model_inf(mobilenet_s, r_image)
        # 4-4
        # emotion_ff = ff_model_inf(mobilenet_sup, mobilenet_neg, r_image)
        # 7-4
        # emotion_sf = sf_model_inf(mobilenet_s, mobilenet_neg, r_image)
        print('\nThis person is {} (Model: 7)'.format(emotion_s))
        # print('This person is {} (4-4)'.format(emotion_ff))
        # print('This person is {} (7-4)\n'.format(emotion_sf))
        cv2.imshow('frame',gray)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
