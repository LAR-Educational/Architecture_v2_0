



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
            
            if  os.path.exists(self.path + "group_list.csv"):
                
                data = pd.read_csv(self.path + "group_list.csv")
                self.group_list = data['Groups'].tolist()
                

            if not os.path.exists(self.path + "/Groups"): 
                os.mkdir(self.path + "/Groups")
                data = pd.DataFrame(columns=['Groups'])
                data.to_csv(self.path + "group_list.csv")

                
        else:  
            os.mkdir(self.path)  
            os.mkdir(self.path + "group_list.csv")
            os.mkdir(self.path + "/Groups")
            self.index_table = pd.DataFrame(columns=['Id', 'Date', 'Group', 'Student Name'])
            self.index_table.to_csv(self.index_path, index=False)

        
        self.load_evaluations_list()
        
        
        self.size = len(self.index_table.index)

        #print self.index_table


    def load_eval(self, path):
        try:
            f = open(path, 'rb')
            tmp_dict = cPickle.load(f)
            f.close()
            return tmp_dict          
        except:
            print "Path {} not found! Evaluation not opened".format(path)
            raise


        #self.__dict__.update(tmp_dict) 


    def save_eval(self, eval, path):
        f = open(path, 'wb')
        cPickle.dump(eval, f, 2)
        f.close()





    def load_evaluations_list(self):
        
        for item in self.index_table.Id:#['Id']:
            #print item
            try:
                self.evaluations_list.append(self.load_eval( os.path.join(self.path,str(item),str(item)+".eval")))
            except:
                print "ERROR IN LOADING EVAL NUMBER", item
        
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




    def add_evaluation_group(self, new_group):   
        
        try:
            self.group_list.append(new_group) 
            
            data = pd.DataFrame(self.group_list, columns=['Groups'])
            
            data.to_csv(self.path + "group_list.csv", index=False) 

            return True
        except:
            raise("ERROR ENTERING GROUP")

class GroupStatus:

    def __init__(self, 
                id,
                name,
                path = None,
                group_name = None,
                durations= None,
                dur_av = None,
                dur_sd = None,    
                measures= None,
                participants= None,
                users_right_rate= None,
                users_accuracy= None,
                users_wrong_rate= None,
                system_right_rate= None,
                system_accuracy= None,
                system_wrong_rate= None,
                obs = ""):


        if durations is None:
            self.durations = []        
        
        if measures is None:
            self.mearues = [[],[],[],[],[]]        
        
        self.id = id
        self.name = name
        self.group_name = group_name
        self.path = path
        self.dur_av = dur_av
        self.dur_sd = dur_sd
        self.participants= participants
        self.users_right_rate= users_right_rate
        self.users_accuracy= users_accuracy
        self.users_wrong_rate= users_wrong_rate
        self.system_right_rate= system_right_rate
        self.system_accuracy= system_accuracy
        self.system_wrong_rate= system_wrong_rate
        self.obs = obs
        self.graphs_trans ={
            'User Validation':'',
            'System Validation':'',
            'User Accuracy':'',
            'System Accuracy':''
                
        }


        #self.__dict__.update(tmp_dict) 


    # def save_group_eval(self, groupStatus, path):
    #     f = open(path, 'wb')
    #     cPickle.dump(groupStatus, f, 2)
    #     f.close()

    def save_group_eval(self, path):
        f = open(path, 'wb')
        cPickle.dump(self, f, 2)
        f.close()


def load_group_eval(path):
    f = open(path, 'rb')
    tmp_dict = cPickle.load(f)
    f.close()

    return tmp_dict          


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
                int_name=None,
                user_dif_profile=None,
                validation=False,
                path=None,
                stats = None,
                ans_threshold=None):

        self.id=id
        self.date=date
        self.path=path
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
        self.int_name=int_name
        self.user_dif_profile=user_dif_profile
        self.validation=validation
        self.stats=stats 
        self.ans_threshold=ans_threshold
               

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

    def __init__(self, given_ans=None, time2ans=None, started = None,
                 finished = None, system_consideration=-1,
                 supervisor_consideration=-1, system_was=-1, ans_dist=None,
                 alpha=None, beta=None, gama=None, fvalue=None, profile=None,
                 read_values=None):
        self.given_ans=given_ans
        self.time2ans=time2ans
        #self.answered_at_time = answered_at_time
        self.system_consideration=system_consideration
        self.supervisor_consideration=supervisor_consideration
        self.system_was=system_was
        self.started = started
        self.finished = finished
        self.ans_dist=ans_dist
        #self.ans_threshold=ans_threshold
        self.alpha=alpha
        self.beta=beta 
        self.gama=gama 
        self.fvalue=fvalue 
        self.profile=profile
        self.read_values=read_values



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
    
    print "YOU ARE IN THE WRONG WINDOWN"
    #main()