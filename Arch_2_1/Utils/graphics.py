
import sys
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# ----------------- Group Assessment

def generate_graphics(data, window, filename, topics_rangeyer):
    pass
    """   
    Function to create group graphics
        data = pandas dataframe with datas
        window =  mian window with componets
        filename = save the name of the evaluation file
        topics_range  = content range as list [first, last]
        displayer = the label to plot the pixmap
    """

    '''
    #def group_eval_generate_graphics(self):

        data = self.group_eval_data_table

        int_name = data["Interaction_name"][0]

        aux_int = self.interact_database.load_interact(self.act.path+"/Interactions/"+int_name+".int")
        list_content_name = aux_int.data.loc[aux_int.data["Type"]=="Content"]
        list_content_name = list_content_name["Name"].tolist()

        max_quest = data["Question_number"].unique() # 6 if total

        max_quest =np.sort(max_quest) #.sort()


        mat = np.zeros((5,len(max_quest)))

        #my_xticks = ["V.E. 1", "V.E. 2", "V.E. 3"]#, "D. 4", "D. 5", "D. 6"]
        my_xticks = []
        
        k = 0
        for topic in list_content_name:

            for i in max_quest:


                a1 = data[ (data['Question_number']==i) & (data['Dificult']==1) & (data['Topic']==topic) ] 
                a2 = data[ (data['Question_number']==i) & (data['Dificult']==2) & (data['Topic']==topic) ] 
                a3 = data[ (data['Question_number']==i) & (data['Dificult']==3) & (data['Topic']==topic) ] 
                a4 = data[ (data['Question_number']==i) & (data['Dificult']==4) & (data['Topic']==topic) ] 
                a5 = data[ (data['Question_number']==i) & (data['Dificult']==5) & (data['Topic']==topic) ] 
                


                i = int(i)

                mat[0,k] = len(a1.index)
                mat[1,k] = len(a2.index)
                mat[2,k] = len(a3.index)
                mat[3,k] = len(a4.index)
                mat[4,k] = len(a5.index)
                
                my_xticks.append(str(QString(topic)) + "_" + str(i))
                k+=1


        cor2 = [ 'paleturquoise', 'cyan','springgreen', 'green', 'black'] #darkgreen']

        
        plt.figure(1)

        #x = [1, 2, 3, 4, 5, 6]
        labels = range(1,len(my_xticks)+1) 	
        x=range(1,len(my_xticks)+1)
        

        plt.xticks(x, my_xticks)

        print labels
        #return 
        for i in range(5):

            y = mat[i]
            plt.plot(x, y, 'o--', color=cor2[i], markersize=10, label=i+1)
            for a,b in zip(x, y): 
                plt.text(a+0.15, b-0.1, str(int(b)))	
                
                


            # for j in range(5):
            # 	x=(i-2*w)+1
            # 	y = mat[i,j]
            # 	plt.plot(x, y, '--', color=cor[j], markersize=10)
                # for a,b in zip(x, y): 
                # 	plt.text(a-0.05, b+1.5, str(b))
                

        plt.legend(title='Difficulty', loc='upper right', 
            numpoints = 1,
            shadow=True,
            handlelength=1.5, 
            fontsize=12)


        plt.xlim(0.8,len(x)+.5)
        plt.ylim(0,(mat[2,0])*2)

        plt.title("Adaptation timeline in 2nd set", fontsize=32)

        plt.xlabel("Topic_Question Number", fontsize=18)
        plt.ylabel("Number of occurrences", fontsize=22)
        plt.show()


    def group_eval_performance_graph(self):
    '''

def users_group_eval(window, df,filename):
    #df = self.group_eval_data_table
    filename = str(filename)
    print filename
    #int_name = df["Interaction_name"][0]

    #aux_int = window.interact_database.load_interact(window.act.path+"/Interactions/"+int_name+".int")
    #aux_int ='3q' 
    #list_content_name = aux_int.data.loc[aux_int.data["Type"]=="Content"]
    list_content_name = df["Topic"].unique()
    
    ret = []

    #list_content_name = list_content_name["Name"].tolist()

    max_quest = df["Question_number"].unique() # 6 if total

    max_quest =np.sort(max_quest) #.sort()

    sys_good = []
    sys_bad =[]
    miss = []
    sup_good=[]
    sup_bad=[]
    my_xticks = []
    
    k = 0
    for topic in list_content_name:

        for i in max_quest:
            i = int(i)
            topic = str(topic)
            yg = df[ (df['Question_number']==i) & (df['Sys_was']==1) & (df['Topic']==topic) ] 
            yb = df[ (df['Question_number']==i) & (df['Sys_was']==0) & (df['Topic']==topic) ] 
            pg = df[ (df['Question_number']==i) & (df['Sup_ans']==1) & (df['Topic']==topic) ] 
            pb = df[ (df['Question_number']==i) & (df['Sup_ans']==0) & (df['Topic']==topic) ] 
            sys_good.append( len(yg.index) )
            sys_bad.append( len(yb.index) )
            sup_good.append( len(pg.index) )
            sup_bad.append( len(pb.index) )

            m  = df[ (df['Question_number']==i) & (df['Sys_was']<0)  & (df['Topic']== topic) ] 
            miss.append( len(m.index) )
        
            my_xticks.append(str(QString(topic)) + "_" + str(i))
            k+=1


    # print sys_good
    # print sys_bad
    # print sup_good
    # print sup_bad

    #return 

    #x = [1, 2, 3, 4, 5, 6]
    #my_xticks = ["V.E. 1", "V.E. 2", "V.E. T3", "D. 1", "D. 5", "D. 6"]
    x = range(1,len(my_xticks)+1)

    #'''
    plt.figure(1)

    #plt.subplot(221)

    #plt.subplot(121)
    plt.xticks(x, my_xticks)
    y = sys_good
    plt.plot(x, y, 'o--', color='g',  markersize=12, label="System's correct classifications")
    for a,b in zip(x, y): 
        plt.text(a, b, str(b))

    y=sys_bad
    plt.plot(x, y,  's--', color='r', markersize=12, label="System's wrong classifications")
    for a,b in zip(x, y): 
        plt.text(a, b, str(b))

    # y=miss
    # plt.plot(x, y,  'x--', color='y', markersize=12, label="Listening problem")
    # for a,b in zip(x, y): 
    # 	plt.text(a+0.18, b-0.2, str(b))


    plt.legend(loc='upper left', numpoints = 1,#('System right ','System Wrong ','Students right answers','Students wrong answers'),
        #shadow=True,
        #loc=(0.01, 0.8),
        #handlelength=1.5, 
        fontsize=12)
    
    plt.xlim(0,len(my_xticks)+1)
    #plt.ylim(0, len(sys_good[0]+sys_bad[0]))
    #plt.ylim(0, len(sys_good)+len(sys_bad))
    plt.ylim(0, (sys_good[0])+(sys_bad[0])+5)

    plt.title("System Classifications", fontsize=32)

    plt.xlabel("Topic_Question Number", fontsize=16)
    plt.ylabel("Number of occurrences", fontsize=20)
    sys_val = filename + "_sys_val.png"
    plt.savefig(sys_val)
    
    #plt.show()
    
    #return
    plt.close()

    plt.figure(1)
    
    #plt.subplot(222)
    plt.xticks(x, my_xticks)

    y=sup_good
    plt.plot(x, y, 'o--', color='b', markersize=12, label="Classified as right")
    for a,b in zip(x, y): 
        plt.text(a-0.05, b+1.0, str(b))

    y=sup_bad
    plt.plot(x, y, 's--', color='r', markersize=12, label="Classified as wrong")
    for a,b in zip(x, y): 
        plt.text(a-0.081, b-1.9, str(b))
    
    y=miss
    plt.plot(x, y,  'x--', color='y', markersize=12, label="Listening problem")
    for a,b in zip(x, y): 
        plt.text(a+0.18, b-0.2, str(b))

    
    plt.legend(loc='upper right', numpoints = 1,#('System right ','System Wrong ','Students right answers','Students wrong answers'),
        #shadow=True,
        #loc=(0.01, 0.8),
        #handlelength=1.5, 
        fontsize=12)

    #print sum(sys_good), sum(sys_bad)
    
    # plt.xlim(0,7)
    # plt.ylim(-1,25)
    plt.xlim(0,len(my_xticks)+1)
    plt.ylim(0, (sys_good[0])+(sys_bad[0])+5)
    #plt.ylim(0, 300)#len(sys_good)+len(sys_bad))

    # plt.title("System Classifications", fontsize=32)

    # plt.xlabel("Topic_Question Number", fontsize=16)
    # plt.ylabel("Number of occurrences", fontsize=20)
    # plt.grid(True, linewidth=.15)
    
    plt.title("Supervisor Classifications", fontsize=32)

    plt.xlabel("Topic_Question Number", fontsize=16)
    plt.ylabel("Number of occurrences", fontsize=20)
    plt.grid(True, linewidth=.15)
    user_val=filename + "_user_val.png"
    plt.savefig(user_val)
    plt.close()

# ----------------------------- PIEs

    ur = df[df['Sup_ans']==1].index.size 	# sys right/student understood/system understood
    uw = df[df['Sup_ans']==0].index.size
    um = df[df['Sup_ans']==-1].index.size


    colors = ['paleturquoise', 'lightcoral', 'lemonchiffon', 'gold', 'lightskyblue']
    
    if um == 0:
        sizes=[ur,uw]
        labels = [" Right \n Ansers", "Wrong \nAnswers"] 
        explode = [0.1,0]

    else:
        labels = [" Right \n Ansers", "Wrong \nAnswers", "Listening \nProblems"] 
        sizes = [ur,uw,um]
        explode = [0.1,0,0]

    plt.rcParams['font.size'] = 16.0

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors= colors,
            shadow=True, startangle=90, explode=explode)

    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title("Users Accuracy", fontsize=35, y =1.03)
    user_ac=filename + "_user_acc.png"
    plt.savefig(user_ac)
    #plt.show()
    plt.close()

    plt.figure(1)

    sr = df[df['Sys_was']==1].index.size 	# sys right/student understood/system understood
    sw = df[df['Sys_was']==0].index.size
    sm = df[df['Sys_was']==-1].index.size

    if sm ==0:
        labels = [" Right \n Classifications", "Wrong \nClassifications"] 
        sizes = [sr,sw]
        explode = [0.1,0]
    else:
        labels = [" Right \n Classifications", "Wrong \nClassifications", "Listening \nProblems"] 
        sizes = [sr,sw,sm]
        explode = [0.1,0,0]

    plt.rcParams['font.size'] = 16.0

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors= colors,
            shadow=True, startangle=90, explode=explode)

    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title("System Accuracy", fontsize=35, y =1.03)
    sys_ac=filename + "_sys_acc.png"
    plt.savefig(sys_ac)
    #plt.show()
    plt.close()

    ret.append(user_val)
    ret.append(sys_val)
    ret.append(user_ac)
    ret.append(sys_ac)

    return ret


if __name__=="__main__":
    pass#users_group_eval("",pd.read_csv(""),"")