



import os
import pandas as pd
from pprint import pprint
import cPickle
from shutil import rmtree
import face_recognition

import cv2



class UserDatabase():

    def __init__(self):
        #print "HI 2"
        self.path = "Usuarios/"
        #print len(os.listdir(self.path))
        self.index_path = self.path + "index_table.csv"
        self.index_table = pd.DataFrame()
        self.users =[]
        self.known_face_encodings = []
        self.known_face_names = []

        if os.path.exists(self.index_path):
            self.index_table = pd.read_csv(self.index_path)
            #print self.index_table
            # print "SIZE:", len(self.index_table.index)

        else:    
            self.index_table = pd.DataFrame(columns=['Id', 'First Name', 'Last Name'])
            self.index_table.to_csv(self.index_path, index=False)

        
        self.load_users_list()
        
        
        self.size = len(self.index_table.index)

        #print self.index_table



    def load_users_list(self):
        
        for item in self.index_table.Id:#['Id']:
            #print item
            self.users.append(self.load_user( os.path.join(self.path,str(item),str(item)+".data")))
        
        
        #print self.users
        
        


    def insert_user(self, new_user):
       
        #create path
        path = self.path + str(new_user.id)
        if os.path.exists(path):
            #raise NameError('Trying to insert user with id "{}". User already exists!'.format(new_user.id))
            self.save_user(new_user, path +"/" +str(new_user.id)+".data")
            self.index_table.to_csv(self.index_path, index=False)
            self.index_table.loc[self.index_table.Id==new_user.id] =[new_user.id, new_user.first_name,new_user.last_name]
            self.index_table.to_csv(self.index_path, index=False)
            print "USER EXIST. UPDATING"
            return -1
        
        else:
            #create paths and images
            os.mkdir(path)
            os.mkdir(path+"/imgs")
            #insert in table
            self.index_table.loc[self.size] =[new_user.id, new_user.first_name,new_user.last_name]
            self.size += 1
            self.users.append(new_user)
            print "USER INSERT DONE"

            self.save_user(new_user, path +"/" +str(new_user.id)+".data")
            self.index_table.to_csv(self.index_path, index=False)
            #print self.index_table
            return 1

    # NAO ESTA TIRANDO O USER DA LISTA DE USUARIOS DA RAM
    # APENAS QUANDO REINICIALIZA O PROGRAMA - Resolvi de um jeito bem porco.
    def delete_user(self, new_user):
        #delete path
        #create path
        path = self.path + str(new_user.id)
        
        if not os.path.exists(path):
            raise NameError('Trying to delete user with id "{}". User NOT exists!'.format(new_user.id))
            #print "USER EXIST"
        
        #else:
        #create paths and images
        rmtree(path)
        #insert in table
        #self.save_user(new_user, path +"/" +str(new_user.id)+".data")
        self.index_table = self.index_table[self.index_table.Id != new_user.id]
        self.size-=1
        print "DELETE DONE"
        #print self.index_table
        self.index_table.to_csv(self.index_path, index=False)
        #self.users.remove()
        #delete table
        #pass
        self.load_users_list()

    def load_user(self, path):
        f = open(path, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()

        return tmp_dict          

        #self.__dict__.update(tmp_dict) 


    def save_user(self, user, path):
        f = open(path, 'wb')
        cPickle.dump(user, f, 2)
        f.close()

    
    def generate_encodings(self):

        path = "images"
        files = os.listdir(path)
    
        for item in files:
            aux = face_recognition.load_image_file(path +"/"+ item)
            aux_encoding = face_recognition.face_encodings(aux)[0]
            self.known_face_names.append(item.replace(".png",""))
            self.known_face_encodings.append(aux_encoding)

        #print len(self.known_face_names)
    
    
    def face_recognition(self, frame):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        #while True:
        # Grab a single frame of video
        #ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        name = None

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        #cv2.imshow('Video', frame)
        return frame, name




class User():

    def __init__(self, id, first_name, last_name, bday='None',
                 scholl_year='None', picture='None', preferences={}, img = None, creation_date=None):

        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.bday=bday
        self.scholl_year=scholl_year
        self.picture=picture
        self.preferences=preferences
        self.pref_index = ['sport', 'team', 'toy', 'game', 'dance', 'music', 'hobby','food']
        self.img = img
        self.creation_date = creation_date
    
    
    def setPreferences(self, sport='None', team='None', toy='None', game='None', 
                        dance='None', music='None', hobby='None', food='None'):
        self.preferences['sport']=sport
        self.preferences['team']=team
        self.preferences['toy']=toy
        self.preferences['game']=game
        self.preferences['dance']=dance
        self.preferences['music']=music
        self.preferences['hobby']=hobby
        self.preferences['food']=food


    def add_preference(self, key, item):

        if key not in self.pref_index:

            raise NameError('Trying to insert key "{}" in user preference. Key not valid!'.format(key))

        else:

            self.preferences[key] = item 


