import os
import pickle
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
            self = load(self.file_name)

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


    def save(self):
        print "Saving"
        with open(self.file_name, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)


    def load(self):
        print "Loading"
        
        self = load(self.file_name)
        # with open(self.file_name, 'rb+') as f:
        #     self = pickle.load(f)




def save(svc):
    print "Saving"
    with open(svc.file_name, 'wb') as f:
        pickle.dump(svc, f, pickle.HIGHEST_PROTOCOL)


def load(path):
    print "Loading"
    with open(path, 'rb+') as f:
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

    print "dps"

    svc.printClass()

    #save(svc)

    svc.save()

    svc1 = SystemVariablesControl()

    svc1.printClass()

    svc1 = load(svc1.file_name)
    #svc1.load()

    print "svc1"
    svc1.printClass()


    #sys_control = {'test':1}

    #print sys_control





if __name__=="__main__":
    main()   











