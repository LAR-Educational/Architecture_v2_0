import os
import pickle
import cPickle
import pandas as pd
from pprint import pprint








class SystemVariablesControl():
    def __init__(self):
       
        # try:
        #     self = pickle.load(open(".system_control.dat", "rb"))
        # except (OSError, IOError) as e:
        #     self.test = 3
        #     self.file_name = ".system_control.dat"
        #     self.test = 20
        #     self.users_id = None
        #     self.session_id = None
        #     self.evaluation_id = None
        #     self.interaction_id = None
        

        #     pickle.dump(self, open(".system_control.dat", "wb"))

        self.file_name = ".system_control.dat"
        self.test = 20
        self.users_id = None
        self.session_id = None
        self.evaluation_id = None
        self.interaction_id = None

        #return 

        if os.path.exists(self.file_name):
            
            print "File Exists"
            self = load(self)

        else:
            self.users_id = 18001
            self.session_id = 18001
            self.evaluation_id = 18001
            self.interaction_id = 18001
        
            self.save()



    def initi_vals(self):
        
        self.users_id = 18001
        self.session_id = 18001
        self.evaluation_id = 18001
        self.interaction_id = 18001
        
     

    
    
    def printClass(self):
        pprint(vars(self))


    def load(self):
        f = open(self.file_name, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()

        #print tmp_dict          

        self.__dict__.update(tmp_dict) 


    def save(self):
        f = open(self.file_name, 'wb')
        cPickle.dump(self.__dict__, f, 2)
        f.close()



def save(svc):
    print "Saving"
    with open(svc.file_name, 'wb') as f:
        pickle.dump(svc, f, pickle.HIGHEST_PROTOCOL)


def load(svc):
    print "Loading"
    with open(svc.file_name, 'rb+') as f:
        return pickle.load(f)


# class SystemVariablesControl():
#     def __init__(self):
        
#         self.file_name = ".system_control.csv"
#         self.
#         if os.path.exists(self.file_name):
            

#         else:
                








def main():

    svc = SystemVariablesControl()

    svc.printClass()

    svc.initi_vals()

    #svc = load(svc)
    
    svc.load()

    print "dps"

    svc.printClass()

    #save(svc)

    svc.users_id += 1

    svc.save()

    svc.printClass()

    return









if __name__=="__main__":
    main()   











