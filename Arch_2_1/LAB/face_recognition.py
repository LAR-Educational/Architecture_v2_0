import cv2
#os module for reading training data directories and paths
import os
#numpy to convert python lists to numpy arrays as it is needed by OpenCV face recognizers
import numpy as np



#there is no label 0 in our training data so subject name for index/label 0 is empty
subjects = []
face_recognizer = cv2.face.createLBPHFaceRecognizer()
   


def create_db_from_cam(user_name, path='training_data/'  ):


    users_number = len(os.listdir(path))

    print "Registered users:", users_number

    #full_path = path + str(users_number)+ '_'  + user_name
    full_path = path + user_name

    print "Full", full_path
    
    if os.path.exists(full_path):
        print "File exist"
    else:
        print "File DO NOT exist. Creating user directory!"
        os.mkdir(full_path)
    
    list_file = os.listdir(full_path)
    counter = len(list_file)

    print "Found {} entries in path with names {}.".format(counter, list_file)

    #return 1

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame

        #

        face, rect = detect_face(frame)
    
        #print "face:", face


        key = cv2.waitKey(1)

        #if key != -1:
            #print "KEY = ", key
            #print "ord", ord('q')

        if face is not None:
            
            
            if (key == 1048691):# and (face is not None):
                img_name = full_path+"/" +str(counter)+".jpg"
                cv2.imwrite(img_name, frame)
                print "Write image", img_name
                counter+=1
            #else:
                #print "FACE NOT DETECT! IMAGE NOT SAVED!"       
            draw_rectangle(frame, rect)
            
        cv2.imshow('Images of user ' + user_name, frame)


        if key == 1048689:
            print "Breaking"
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    print "\nEnding process with total of {} images on path\n\n".format(counter)



def identifier_from_cam():
    
    print("Preparing data...")
    faces, labels = prepare_training_data("training_data")
    print("Data prepared")
    
    #create our LBPH face recognizer 
    global face_recognizer
    face_recognizer = cv2.face.createLBPHFaceRecognizer()
    
    # or use EigenFaceRecognizer by replacing above line with 
    # face_recognizer = cv2.face.createEigenFaceRecognizer()
    
    # or use FisherFaceRecognizer by replacing above line with 
    # face_recognizer = cv2.face.createFisherFaceRecognizer()

    #train our face recognizer of our training faces
    face_recognizer.train(faces, np.array(labels))

    print("Predicting images...")

    #load test images
    #test_img1 = cv2.imread("0.jpg")

    #test_img2 = cv2.imread("test2.jpg")

    #show_face(test_img1)

    #return

    sub_count = [0] * len(subjects) #dict( (subject,0) for subject in subjects)

    #for i in range():
        #sub_count[]


    print sub_count

    #return

    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        face, rect = detect_face(frame)
 
        if face is not None:
            #predict the image using our face recognizer 
            label= face_recognizer.predict(face)
            #print "LABEL", label
            #get name of respective label returned by face recognizer
            label_text = subjects[label[0]]
            
            #draw a rectangle around face detected
            draw_rectangle(frame, rect)
            #draw name of predicted person
            draw_text(frame, label_text, rect[0], rect[1]-5)
            
            sub_count[label[0]] += 1

            #return img

        #img = predict(frame)
        
        key = cv2.waitKey(1)

        #if key != -1:
            #print "KEY = ", key
            #print "ord", ord('q')

        # if img is None:
            
        #     img = frame
            
            
        cv2.imshow('Window', frame)


        if (key == 1048691):
            _max = sub_count.index(max(sub_count))
            print "MAX", _max
            print sub_count
            sub_count * 0
            print "FINAL", subjects[_max]

        if key == 1048689:
            print "Breaking"
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    print "\nEnding process!\n\n"





def detect_mult(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects


def detect_face(img):
    #convert the test image to gray scale as opencv face detector expects gray images
    
    #print "IMG", img

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Nada",gray)
    # cv2.waitKey(0)
    

    #load OpenCV face detector, I am using LBP which is fast
    #there is also a more accurate but slow: Haar classifier
    face_cascade = cv2.CascadeClassifier('/home/tozadore/opencv/data/lbpcascades/lbpcascade_frontalface.xml')

    #let's detect multiscale images(some images may be closer to camera than others)
    #result is a list of faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    #if no faces are detected then return original img
    if (len(faces) == 0):
        return None, None

    #under the assumption that there will be only one face,
    #extract the face area
    x, y, w, h = faces[0]

    #return only the face part of the image
    return gray[y:y+w, x:x+h], faces[0]



#this function will read all persons' training images, detect face from each image
#and will return two lists of exactly same size, one list 
#of faces and another list of labels for each face
def prepare_training_data(data_folder_path):

    #------STEP-1--------
    #get the directories (one directory for each subject) in data folder
    dirs = os.listdir(data_folder_path)

    #list to hold all subject faces
    faces = []
    #list to hold labels for all subjects
    labels = []

    print "Dirs:", dirs

    #let's go through each directory and read images within it
    for dir_name in dirs:

        print "Dir_name:", dir_name

        #our subject directories start with letter 's' so
        #ignore any non-relevant directories if any
        #if not dir_name.startswith("s"):
        #    continue;

        #------STEP-2--------
        #extract label number of subject from dir_name
        #format of dir name = slabel
        #, so removing letter 's' from dir_name will give us label
        #label = int(dir_name.replace("s", ""))
        #label, name = dir_name.split('_')
        
        label = len(subjects)
        subjects.append(dir_name)
        #print "label" , label, name
        #global subjects

        print "label:", label, "subject", subjects[label]
        #print subjects

        #break

        #build path of directory containing images for current subject subject
        #sample subject_dir_path = "training-data/s1"
        subject_dir_path = data_folder_path + "/" + dir_name

        #get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)

        #------STEP-3--------
        #go through each image name, read image, 
        #detect face and add face to list of faces
        for image_name in subject_images_names:

            #ignore system files like .DS_Store
            if image_name.startswith("."):
                continue;

            #build image path
            #sample image path = training-data/s1/1.pgm
            image_path = subject_dir_path + "/" + image_name

            #read image
            image = cv2.imread(image_path)

            #display an image window to show the image 
            #cv2.imshow("Training on image...", image)
            #cv2.waitKey(2)

            #detect face
            face, rect = detect_face(image)


        #------STEP-4--------
        #for the purpose of this tutorial
        #we will ignore faces that are not detected
        if face is not None:
            #add face to list of faces
            faces.append(face)
            #add label for this face
            labels.append(label)

        #cv2.destroyAllWindows()
    
    
    cv2.waitKey(20)
    cv2.destroyAllWindows()

    return faces, labels



#according to given (x, y) coordinates and 
#given width and heigh
def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
#function to draw text on give image starting from
#passed (x, y) coordinates. 
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

	
#this function recognizes the person in image passed
#and draws a rectangle around detected face with name of the 
#subject
def predict(test_img):
    #make a copy of the image as we don't want to change original image
    img = test_img.copy()
    #detect face from the image
    face, rect = detect_face(img)
 
    if face is not None:
        #predict the image using our face recognizer 
        label= face_recognizer.predict(face)
        print "LABEL", label
        #get name of respective label returned by face recognizer
        label_text = subjects[label[0]]
        
        #draw a rectangle around face detected
        draw_rectangle(img, rect)
        #draw name of predicted person
        draw_text(img, label_text, rect[0], rect[1]-5)
        
        return img

    else:
        return None


def show_face(img):

    face, rect = detect_face(img)
    
    print "face:", face

    if face is None:
        print "Face not detected!"
        return 0

    draw_rectangle(img, rect)

    cv2.imshow("Face", img)
    cv2.waitKey(0)




def main():

    user_name = raw_input("Enter with user name: ")
    create_db_from_cam(user_name)
    
    #prepare_training_data('training_data/')    
    
    #print subjects


def omain():

    #data will be in two lists of same size
    #one list will contain all the faces
    #and the other list will contain respective labels for each face
    print("Preparing data...")
    faces, labels = prepare_training_data("training_data")
    print("Data prepared")
    
    #print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))



    print "subjects:", subjects 

    #create our LBPH face recognizer 
    global face_recognizer
    face_recognizer = cv2.face.createLBPHFaceRecognizer()
    
    # or use EigenFaceRecognizer by replacing above line with 
    # face_recognizer = cv2.face.createEigenFaceRecognizer()
    
    # or use FisherFaceRecognizer by replacing above line with 
    # face_recognizer = cv2.face.createFisherFaceRecognizer()

    #train our face recognizer of our training faces
    face_recognizer.train(faces, np.array(labels))

    print("Predicting images...")

    #load test images
    test_img1 = cv2.imread("0.jpg")

    #test_img2 = cv2.imread("test2.jpg")

    #show_face(test_img1)

    #return

    #perform a prediction
    predicted_img1 = predict(test_img1)
    #predicted_img2 = predict(test_img2)
    print("Prediction complete")

    #display both images
    cv2.imshow("Result", predicted_img1)
    #cv2.imshow(subjects[2], predicted_img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_rects(img, rects, color=(255, 0, 0)):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)



def multiple_detection():

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    print("Preparing data...")
    train_data, labels = prepare_training_data("training_data")
    print("Data prepared")
    
    global face_recognizer
   
    #create our LBPH face recognizer 
    face_recognizer = cv2.face.createLBPHFaceRecognizer()
    
    # or use EigenFaceRecognizer by replacing above line with 
    # face_recognizer = cv2.face.createEigenFaceRecognizer()
    
    # or use FisherFaceRecognizer by replacing above line with 
    # face_recognizer = cv2.face.createFisherFaceRecognizer()

    #train our face recognizer of our training faces
    face_recognizer.train(train_data, np.array(labels))

    cap = cv2.VideoCapture(0)
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #faces = faceCascade.detectMultiScale(frame, 1.3, 5)
        faces = faceCascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
        
        #detected_faces = []

        if len(faces) != 0:

            #fnum = 0 
            for rect in faces:

                x, y, w, h = rect

                face = img[y:y+w, x:x+h]

                #predict the image using our face recognizer 
                label = face_recognizer.predict(face)
                print "LABEL", label
                #get name of respective label returned by face recognizer
                label_text = subjects[label[0]]
                
                #draw a rectangle around face detected
                draw_rectangle(frame, rect)
                #draw name of predicted person
                draw_text(frame, label_text, rect[0], rect[1]-5)

                #detected_faces.append(face)
                #cv2.imshow(label_text , face)
                
                
        key = cv2.waitKey(1)

        #print len(faces)

        cv2.imshow('Window', frame)

        if (key == 1048691):
            pass

        if key == 1048689:
            print "Breaking"
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    print "\nEnding process!\n\n"





if __name__=="__main__":
    #main()
    #identifier_from_cam()
    multiple_detection()