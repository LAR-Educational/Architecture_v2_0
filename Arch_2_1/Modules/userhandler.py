



import os
import pandas as pd
from pprint import pprint
import cPickle
from shutil import rmtree

class UserDatabase():

    def __init__(self):
        #print "HI 2"
        self.path = "Usuarios/"
        #print len(os.listdir(self.path))
        self.index_path = self.path + "index_table.csv"
        self.index_table = pd.DataFrame()
        self.users =[]

        if os.path.exists(self.index_path):
            self.index_table = pd.read_csv(self.index_path)
            #print self.index_table
            # print "SIZE:", len(self.index_table.index)

        else:    
            self.index_table = pd.DataFrame(columns=['Id', 'First Name', 'Last Name'])
            self.index_table.to_csv(self.index_path, index=False)

        
        self.load_users_list()
        
        
        self.size = len(self.index_table.index)

        print self.index_table



    def load_users_list(self):
        
        for item in self.index_table.Id:#['Id']:
            print item
            self.users.append(self.load_user( os.path.join(self.path,str(item),str(item)+".data")))
        
        
        print self.users
        
        


    def insert_user(self, new_user):
       
        #create path
        path = self.path + str(new_user.id)
        if os.path.exists(path):
            raise NameError('Trying to insert user with id "{}". User already exists!'.format(new_user.id))
            #print "USER EXIST"
        
        #else:
        #create paths and images
        os.mkdir(path)
        os.mkdir(path+"/imgs")
        #insert in table
        self.save_user(new_user, path +"/" +str(new_user.id)+".data")
        self.index_table.loc[self.size] =[new_user.id, new_user.first_name,new_user.last_name]
        self.size += 1

        self.index_table.to_csv(self.index_path, index=False)
        print "USER INSERT DONE"
        print self.index_table
        


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
        print self.index_table
        self.index_table.to_csv(self.index_path, index=False)
        
        #delete table
        #pass


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







class User():

    def __init__(self, id, first_name, last_name, bday='None',
                 scholl_year='None', picture='None', preferences={}, img = None):

        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.bday=bday
        self.scholl_year=scholl_year
        self.picture=picture
        self.preferences=preferences
        self.pref_index = ['sport', 'team', 'toy', 'game', 'dance', 'music', 'hobby','food']
        self.img = img
    
    
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




def main():

    #print "HI 1"
    udb = UserDatabase()

    u1 = User(3,"2dme","222t")


    u1.setPreferences()

    u1.preferences['music'] = "Avicci"

    u1.add_preference('food',"FISHHH")

    #pprint(vars(u1))


    #udb.insert_user(u1)
    #udb.delete_user(u1)



if __name__=='__main__':
    main()          