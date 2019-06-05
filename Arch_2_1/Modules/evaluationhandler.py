



import os
import pandas as pd
from pprint import pprint
import cPickle
from shutil import rmtree
import face_recognition

import cv2



class EvaluationDatabase():

    def __init__(self):
        #print "HI 2"
        self.path = "Evaluations/"
        #print len(os.listdir(self.path))
        self.index_path = self.path + "index_table.csv"
        self.index_table = pd.DataFrame()
        self.evaluations_list = []
        self.group_list = []
        #self.known_face_encodings = []
        ##s#elf.known_face_names = []

        if os.path.exists(self.index_path):
            self.index_table = pd.read_csv(self.index_path)
            
            if  os.path.exists(self.path + "group_list.txt"):
                inF = open(self.path + "group_list.txt", "r")
                for line in inF:
                    self.group_list.append(line)
                    
                inF.close()    
                    
                print "LENNNN", len(self.group_list)
            #print self.index_table
            # print "SIZE:", len(self.index_table.index)
            
        else:  
            os.mkdir(self.path)  
            self.index_table = pd.DataFrame(columns=['Id', 'Date', 'Student Name'])
            self.index_table.to_csv(self.index_path, index=False)

        
        self.load_evaluations_list()
        
        
        self.size = len(self.index_table.index)

        #print self.index_table



    def add_evaluation_group(self, new_group):   
        
        try:
            self.group_list.append(new_group) 
            
            outF = open(self.path + "group_list.txt", "w")
        
            for line in self.group_list:
            # write line to output file
                outF.write(line)
                #outF.write("\n")
            outF.close()
            return True
        except:
            raise("ERROR ENTERING GROUP")

    def load_evaluations_list(self):
        
        for item in self.index_table.Id:#['Id']:
            #print item
            self.evaluations_list.append(self.load_eval( os.path.join(self.path,str(item),str(item)+".eval")))
        
        
        #print self.users
        



    def insert_eval(self, new_eval):
       
        #create path
        path = self.path + str(new_eval.id)
        if os.path.exists(path):
            #raise NameError('Trying to insert user with id "{}". User already exists!'.format(new_user.id))
            self.save_eval(new_eval, path +"/" +str(new_eval.id)+".eval")
            self.index_table.to_csv(self.index_path, index=False)
            #self.index_table.loc[self.index_table.Id==new_eval.id] =[new_eval.id, new_eval.date.toString("dd.MM.yy"), new_eval.user_name]
            #self.index_table.to_csv(self.index_path, index=False)
            print "EVALUATION ALREADY EXIST. UPDATING"
            return -1
        
        else:
            #create paths and images
            os.mkdir(path)
            os.mkdir(path+"/imgs")
            #insert in table
            self.index_table.loc[self.size] =[new_eval.id, new_eval.date.toString("dd.MM.yy"), new_eval.user_name]
            self.size += 1
            self.evaluations_list.append(new_eval)
            print "EVALUATION INSERT DONE"
            self.save_eval(new_eval, path +"/" +str(new_eval.id)+".eval")
            print "PATH", self.index_path
            self.index_table.to_csv(self.index_path, index=False)
            #print self.index_table
            return 1





    # NAO ESTA TIRANDO O USER DA LISTA DE USUARIOS DA RAM
    # APENAS QUANDO REINICIALIZA O PROGRAMA - Resolvi de um jeito bem porco.
    def delete_eval(self, new_eval):
        #delete path
        #create path
        path = self.path + str(new_eval.id)
        
        if not os.path.exists(path):
            raise NameError('Trying to delete evaluation with id "{}". Evalutaion NOT exists!'.format(new_eval.id))
            #return False
            #print "USER EXIST"
        
        #else:
        #create paths and images
        rmtree(path)
        #insert in table
        #self.save_user(new_user, path +"/" +str(new_user.id)+".data")
        self.index_table = self.index_table[self.index_table.Id != new_eval.id]
        self.size-=1
        print "DELETE DONE"
        #print self.index_table
        self.index_table.to_csv(self.index_path, index=False)
        #self.users.remove()
        #delete table
        #pass
        self.load_evaluations_list()

        return True



    def load_eval(self, path):
        f = open(path, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()

        return tmp_dict          

        #self.__dict__.update(tmp_dict) 


    def save_eval(self, eval, path):
        f = open(path, 'wb')
        cPickle.dump(eval, f, 2)
        f.close()




class Evaluation:
    
    def __init__(self, id, 
                date=None, 
                user_id=None, 
                user_name=None, 
                topics=None,
                tp_names=None, 
                duration=None,
                start_time=None,
                end_time=None,
                robot=None,
                supervisor=None,
                obs=None,
                group=None,
                int_id=None,
                user_dif_profile=None,
                validation=False,
                stats = None):

        self.id=id
        self.date=date
        self.user_id = user_id
        self.user_name=user_name
        if topics is None:
            self.topics=[]
        if tp_names is None:
            self.tp_names=[]
        self.duration=duration
        self.start_time=start_time
        self.end_time=end_time
        self.robot=robot
        self.supervisor=supervisor
        self.obs=obs
        self.group=group
        self.int_id=int_id
        self.user_dif_profile=user_dif_profile
        self.validation=validation
        self.stats=stats        

    def insert_topic(self, tp):
        self.topics.append(tp)
   
    

class Topic:

    def __init__(self, concept=None, questions=None, started = None, finished = None):
        self.concept=concept
        if questions is None:
            self.questions=[]
        self.started = started
        self.finished = finished
        
    def insert_question(self, qt):
        self.questions.append(qt)


class Question:

    def __init__(self, question=None, exp_ans=None, attempts=None, started = None, finished = None):
        self.question=question
        self.exp_ans=exp_ans
        if attempts is None:
            self.attempts=[]
        self.started = started
        self.finished = finished

    
    def insert_attempt(self, att):
        self.attempts.append(att)


class Attempt:

    def __init__(self, given_ans=None, time2ans=None, started = None, finished = None, system_consideration=-1,
                    supervisor_consideration=-1, sytem_was=-1):
        self.given_ans=given_ans
        self.time2ans=time2ans
        #self.answered_at_time = answered_at_time
        self.system_consideration=system_consideration
        self.supervisor_consideration=supervisor_consideration
        self.sytem_was=sytem_was
        self.started = started
        self.finished = finished




class Stats:

    def __init__(self, n_topics = -1, qt_tp = -1, time_per_topic = -1, 
                    mistakes  = -1, total_qt = -1,  right_answers  = -1,
                    success_rate  = -1, sys_accuracy  = -1):
        self.n_topics = n_topics 
        self.qt_tp = qt_tp 
        self.time_per_topic = time_per_topic  
        self.mistakes  = mistakes
        self.total_qt = total_qt 
        self.right_answers  = right_answers 
        self.success_rate  = success_rate 
        self.sys_accuracy  = sys_accuracy


def main():
    
    print ""

    ev_test=Evaluation(1,"data")

    att1 = Attempt("giv1", 1.1, True, True, True)
    att2 = Attempt("giv2", 2.2, True, False, False)

    ques = Question()

    print "len 1 ", len(ques.attempts)
    ques.insert_attempt(att1)
    ques.insert_attempt(att2)

    print "len 2", len(ques.attempts)


    print ques.attempts[0].given_ans


if __name__=="__main__":
    main()