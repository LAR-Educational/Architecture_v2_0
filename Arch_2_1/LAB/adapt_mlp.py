

import numpy as np 
import matplotlib.pyplot as plt
from sklearn import svm, metrics, datasets, neural_network, neighbors, naive_bayes
from sklearn.model_selection import GridSearchCV, train_test_split




data = np.loadtxt("mlp.csv", delimiter=',', skiprows=1)

datasize = len(data[:,0])

print datasize

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

# model = mlp


# model = svm.SVC(C=3, kernel='linear')

model = svm.LinearSVC(penalty='l2',loss='hinge', dual=True, tol=1e-5, multi_class='crammer_singer', class_weight='balancede')

# model = neighbors.KNeighborsClassifier(n_neighbors=5)

print "Fitting data"
model.fit(x_train,y_train)

print "Done!\nStarting Evaluation"

y_pred = model.predict(x_test)
print "--- Evaluation done  ---" 
        
print("Classification report for - \n{}:\n{}\n\n".format(
            model, metrics.classification_report(y_test, y_pred)))






# print y
# print data 