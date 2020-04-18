

import numpy as np 
import matplotlib.pyplot as plt
from sklearn import svm, metrics, datasets, neural_network, neighbors, naive_bayes
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import adjusted_rand_score

# measures Rule-Based
# data = np


# data = np.loadtxt("/home/to/Projects/Architecture_v2_0/Arch_2_1/Read_values_RULEBASED.csv", delimiter=',', skiprows=1)

# print data 

# #def f1():

# tp = float(29)
# fp = float(7)
# fn = float(14)



# f1 = 2*tp / (2*tp + fp +fn)


# print "F1", f1



def measures():
    
    # data = np.loadtxt("/home/to/Projects/Architecture_v2_0/Arch_2_1/Read_values_RULEBASED.csv", delimiter=',', skiprows=1)

    t1 = 61 * [-1]
    # tl = 13 * [0] #tl.append( 13 * [0] )
    t2 = 13 * [0]
    t3 = (29+14) * [1] 
    tl = t1 + t2 + t3


    rl = ( (54+10+10)  * [-1]) + ( (7+2+9) * [0]) + ( (24 +1) * [1])   

    fl = ( (53+11+11)  * [-1]) + ( 6 * [0]) + ( (7+29) * [1])   


    #print t3
    print len(rl)
    print len(fl)
    # print t1.append(t2)

    # print adjusted_rand_score(tl,fl)
    # print adjusted_rand_score(tl,rl)



def accuracy():

    data = np.loadtxt("mlp.csv", delimiter=',', skiprows=1)

    # head = data[0,:]
    # print head
    # # x = numpy.delete(x, (0), axis=0)
    # data = np.delete(data, (0), axis=0)
    # # data = data[-0,:]
    
    datasize = len(data[:,0])

    #print datasize

    x_train = data[:int(datasize*0.66),:5]
    y_train = data[:int(datasize*0.66),5]


    # print len(xtrain)
    # print len(ytrain)


    x_test = data[int(datasize*0.66):,:5]
    y_test = data[int(datasize*0.66):,5]


    # X = data[:,:5]
    # Y = data[:,5]

    # xtest = data[]
    # ytest =


    # model = neural_network.MLPClassifier(solver= 'adam', hidden_layer_sizes=(100,100,100), max_iter= 100, momentum=0.1, power_t=0.5)

    # model = mlp


    #model = svm.SVC(C=3, kernel='linear')

    # model = svm.LinearSVC(penalty='l2',loss='hinge', dual=True, tol=1e-5, multi_class='crammer_singer', class_weight='balanced')

    #model = neighbors.KNeighborsClassifier(n_neighbors=5)


    # result = cross_val_score(model, X, Y, cv=10)

    # print result 

    # print np.average(result) , len(result)

    # exit()

    model = RandomForestClassifier(max_depth=5, random_state=0)

    print "Fitting data"
    model.fit(x_train,y_train)


    print "Done!\nStarting Evaluation"

    y_pred = model.predict(x_test)
    print "--- Evaluation done  ---" 
            
    print("Classification report for - \n{}:\n{}\n\n".format(
                model, metrics.classification_report(y_test, y_pred)))

    print model.feature_importances_

    print data 





    # print y
    # print data 




if __name__== "__main__":
    #measures()
    accuracy()




# Classifier & MLP    & SVM   & KNN   &  RFC  & Rule-Based & Fuzzy   \\ \hline
# Precision   & 0.55  &  0.72 &  0.56 &  0.71 &  0.60      &  0.56 \\
# Recall      & 0.65  &  0.82 &  0.55 &  0.78 &  0.53      &  0.53\\
# F-1         & 0.60  &  0.76 &  0.51 &  0.72 &  0.54      &  0.53\\
