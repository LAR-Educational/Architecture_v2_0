

import numpy as np 
import matplotlib.pyplot as plt
from sklearn import svm, metrics, datasets, neural_network, neighbors, naive_bayes
<<<<<<< HEAD
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
=======
from sklearn.model_selection import GridSearchCV, train_test_split
>>>>>>> 8588090925555211825cca553f36ade5016ea42c




data = np.loadtxt("mlp.csv", delimiter=',', skiprows=1)

datasize = len(data[:,0])

print datasize

<<<<<<< HEAD


n1 = np.count_nonzero(data[:,5] ==-1)
n0 = np.count_nonzero(data[:,5] == 0)
nm1 =np.count_nonzero(data[:,5] == 1)



print n1,n0, nm1, n1+n0+nm1

# print ([data[:,5]==-1]==True)
# print data[:,5]==-1
# print data[:,5]==-1

# nm1 = len(data[:5]==-1)
# n0
# n1

#exit()



# x_train = data[:int(datasize*0.66),:5]
# y_train = data[:int(datasize*0.66),5]

# # print len(xtrain)
# # print len(ytrain)


# x_test = data[int(datasize*0.66):,:5]
# y_test = data[int(datasize*0.66):,5]

xtest = data[:,:5]
ytest = data[:,5]


#x_train, x_test, y_train, y_test = 




model = neural_network.MLPClassifier(solver= 'sgd', hidden_layer_sizes=(10,10,10, 10), max_iter= 10000, momentum=0.0, power_t=0.5)
=======
x_train = data[:int(datasize*0.66),:5]
y_train = data[:int(datasize*0.66),5]

# print len(xtrain)
# print len(ytrain)


x_test = data[int(datasize*0.66):,:5]
y_test = data[int(datasize*0.66):,5]

# xtest = data[]
# ytest =


# model = neural_network.MLPClassifier(solver= 'sgd', hidden_layer_sizes=(100,100,100), 
#                                     max_iter= 100, momentum=0.0,
#                                     power_t=0.5)
>>>>>>> 8588090925555211825cca553f36ade5016ea42c

# model = mlp


<<<<<<< HEAD
# model = svm.SVC(C=1, kernel='linear')

# model = svm.LinearSVC(penalty='l2',loss='hinge', dual=True, tol=1e-5, multi_class='crammer_singer', class_weight='balanced')

# model = neighbors.KNeighborsClassifier(n_neighbors=5)





scores = cross_val_score(model, xtest, ytest, cv=10)

print (scores)
print np.average(scores)

exit()














=======
# model = svm.SVC(C=3, kernel='linear')

model = svm.LinearSVC(penalty='l2',loss='hinge', dual=True, tol=1e-5, multi_class='crammer_singer', class_weight='balancede')

# model = neighbors.KNeighborsClassifier(n_neighbors=5)

>>>>>>> 8588090925555211825cca553f36ade5016ea42c
print "Fitting data"
model.fit(x_train,y_train)

print "Done!\nStarting Evaluation"

y_pred = model.predict(x_test)
print "--- Evaluation done  ---" 
        
print("Classification report for - \n{}:\n{}\n\n".format(
            model, metrics.classification_report(y_test, y_pred)))






# print y
# print data 