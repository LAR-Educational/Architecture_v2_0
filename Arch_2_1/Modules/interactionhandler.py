



import os
import pandas as pd
from pprint import pprint
import cPickle
from shutil import rmtree
import face_recognition

import cv2



class InteractionDatabase():

    def __init__(self, act_path):
        #print "HI 2"
        self.path = os.path.join(act_path,"Interactions")
        #print len(os.listdir(self.path))
        # self.index_path = os.path.join(self.path, "index_table.csv")
        # self.index_table = pd.DataFrame()
        # self.interactions_list = []
        #self.known_face_encodings = []
        #self.known_face_names = []

        #  if not os.path.exists(self.index_path):
        #      os.mkdir(self.path)
        
        #     self.index_table = pd.read_csv(self.index_path)
        #     #print self.index_table
        #     # print "SIZE:", len(self.index_table.index)

        # else:    
        #     self.index_table = pd.DataFrame(columns=['Id'])
        #     self.index_table.to_csv(self.index_path, index=False)

        
        # self.load_interactions_list()
        
        
        # self.size = len(self.index_table.index)

        #print self.index_table



    # def load_interactions_list(self):
        
    #     for item in self.index_table.Id:#['Id']:
    #         #print item
    #         self.interactions_list.append(self.load_user( os.path.join(self.path,str(item),str(item)+".interact")))
        
        
        #print self.users
        
        


    # def insert_interact(self, new_interact):
       
    #     #create path
    #     path = self.path + str(new_interact.id)
    #     if os.path.exists(path):
    #         #raise NameError('Trying to insert user with id "{}". User already exists!'.format(new_user.id))
    #         self.save_interact(new_interact, path +"/" +str(new_interact.id)+".interact")
    #         self.index_table.to_csv(self.index_path, index=False)
    #         self.index_table.loc[self.index_table.Id==new_interact.id] =[new_interact.id, new_interact.first_name,new_interact.last_name]
    #         self.index_table.to_csv(self.index_path, index=False)
    #         print "INTERACTION ALREADY EXIST. UPDATING"
    #         return -1
        
    #     else:
    #         #create paths and images
    #         os.mkdir(path)
    #         #os.mkdir(path+"/imgs")
    #         #insert in table
    #         self.index_table.loc[self.size] =[new_interact.id, new_interact.first_name, new_interact.last_name]
    #         self.size += 1
    #         self.interactions_list.append(new_interact)
    #         print "INTERACTION INSERT DONE"

    #         self.save_interactuation(new_user, path +"/" +str(new_interact.id)+".interact")
    #         self.index_table.to_csv(self.index_path, index=False)
    #         #print self.index_table
    #         return 1



    # NAO ESTA TIRANDO O USER DA LISTA DE USUARIOS DA RAM
    # APENAS QUANDO REINICIALIZA O PROGRAMA - Resolvi de um jeito bem porco.
    # def delete_interact(self, new_interact):
    #     #delete path
    #     #create path
    #     path = self.path + str(new_interact.id)
        
    #     if not os.path.exists(path):
    #         raise NameError('Trying to delete interaction with id "{}". Interaction NOT exists!'.format(new_user.id))
    #         #print "USER EXIST"
        
    #     #else:
    #     #create paths and images
    #     rmtree(path)
    #     #insert in table
    #     #self.save_user(new_user, path +"/" +str(new_user.id)+".data")
    #     self.index_table = self.index_table[self.index_table.Id != new_interact.id]
    #     self.size-=1
    #     print "DELETE DONE"
    #     #print self.index_table
    #     self.index_table.to_csv(self.index_path, index=False)
    #     #self.users.remove()
    #     #delete table
    #     #pass
    #     self.load_interactions_list()




    def load_interact(self, path):
        f = open(path, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()

        return tmp_dict          

        #self.__dict__.update(tmp_dict) 


    def save_interact(self, interact, path):
        f = open(path, 'wb')
        cPickle.dump(interact, f, 2)
        f.close()




class Interaction:
    
    def __init__(self, id=0, 
                ques_per_topic=1,
                att_per_ques=1,
                name=None,
                data=None,
                creator=None
                ):

        self.id=id
        self.ques_per_topic=ques_per_topic
        self.att_per_ques = att_per_ques
        self.name=name
        self.data=data
        self.creator=creator

               

