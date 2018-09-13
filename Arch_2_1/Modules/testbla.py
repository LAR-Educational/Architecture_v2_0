import os
import pickle
from pprint import pprint

class SystemVariablesControl():
    def __init__(self):

        self.file_name = ".system_control.dat"
        self.test = 20
        #self.users_id = None
        #self.session_id = None
        s#elf.evaluation_id = None
        #self.interaction_id = None
        
        if os.path.exists(self.file_name):
            
            self.load()

        else:
            self.users_id = 18001
            self.session_id = 18001
            self.evaluation_id = 18001
            self.interaction_id = 18001
            self.save()

    def printClass(self):
        pprint(vars(self))


    def save(self):
        print "Saving"
        with open(self.file_name, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)


    def load(self):
        print "Loading"
        with open(self.file_name, 'rb+') as f:
            self = pickle.load(f)


def main():

    svc = SystemVariablesControl()

    svc.printClass()


if __name__=="__main__":
    main()   