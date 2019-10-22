# -*- coding: utf-8 -*-


from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm, metrics, datasets, neural_network, neighbors, naive_bayes

#from sklearn.neural_network import MLPClassifier

from sklearn.utils import Bunch
from sklearn.model_selection import GridSearchCV, train_test_split

from skimage.io import imread
from skimage.transform import resize

from data_process import Data_process
import cPickle
import os
from time import time

class My_toolkit():

    def __init__(self, work_path):

        self.work_path = os.path.join(work_path, "Vision")
        self.file_name = os.path.join(self.work_path, ".toolkit.info")
        self.tk_db_name = "toolkit.db"
        self.database = None
        self.im_dim = (60,60)
        # self.im_dim = (320,240)
        self.model_type=None
        self.categories=["cubo","esfera","piramide"]
        if os.path.exists(self.file_name):
            self.load()
        else:    
            self.save()



    def load(self):
        f = open(self.file_name, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()
        self.__dict__.update(tmp_dict) 


    def save(self):
        print "--- Saving ---"
        started = time()
        f = open(self.file_name, 'wb')
        cPickle.dump(self.__dict__, f, 2)
        f.close()
        print "--- Save done in {} seconds\n".format(time()-started)

    def load_database_from_file(self):
        f = open(self.tk_db_name, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()
        self.database = tmp_dict 


    def save_database(self):
        f = open(self.tk_db_name, 'wb')
        cPickle.dump(self.database, f, 2)
        f.close()


    def load_database(self):
		
        if not self.database is None:
            print "--- Database already loaded! --- "
        
        elif os.path.exists(os.path.join(self.work_path,  self.tk_db_name)):
            self.database= self.load_database_from_file()
            print "--- Database loaded from file! --- "
        
        else:
            print "--- Generating database from path " + os.path.join(self.work_path, "Images")+" --- "
            print "--- It could take a while"
            started = time()
            self.database = load_image_files(os.path.join(self.work_path, "Images"), self.im_dim)
            print "--- Done! --- \n--- Database generated in {} seconds\n".format(time()-started)
            
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
                self.database.data, self.database.target, test_size=0.3,random_state=109)
    
            #self.save()


    def fit_model(self):
        print "--- Fitting model! It could take a while ---"
        started = time()
        self.model.fit(self.x_train, self.y_train)    
        print "--- Model fit in {} seconds ---\n".format(time()-started) 


    def svm_model(self):

        print "--- Setting SVM model parameters ---"

        param_grid = [
        {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
        ]
        # svc = svm.SVC()
        # self.model = GridSearchCV(svc, param_grid)
        
        #svc = 
        self.model = svm.SVC( gamma=0.0001) 
        
        print "--- SVM model set ---"
        #return self.model


    def mlp_model(self):
        print "--- Setting MLP model parameters ---"

        mlp = neural_network.MLPClassifier(hidden_layer_sizes=(100,10))
        self.model = mlp
        print "--- MLP model set ---\n"
        #return self.model


    def knn_model(self, n_neighbors = 5):
        print "--- Setting KNN model parameters ---"

        knn = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors)
        self.model = knn
        print "--- KNN model set to neighbors = {}---\n".format(n_neighbors)
        #return self.model


    def nayve_model(self):
        print "--- Setting Nayve model parameters ---"

        #nb = naive_bayes.MultinomialNB()
        # nb = naive_bayes.ClassifierMixin()
        nb = naive_bayes.GaussianNB()
        # nb = naive_bayes.BernoulliNB()
        self.model = nb
        print "--- Nayve model set ---\n"
        #r#return self.model


    #def set_model(self, type):

       # if 'svm':



    def evaluate(self):
        print "--- Starting model evaluation ---"
        started = time()
        self.y_pred = self.model.predict(self.x_test)
        print "--- Evaluation done in {} seconds ---".format(time()-started) 
        
        print("Classification report for - \n{}:\n{}\n\n".format(
            self.model, metrics.classification_report(self.y_test, self.y_pred)))





    def save_model(self, model_name):

        print "--- Saving model {}".format(model_name)
        started = time()
        path = os.path.join(self.work_path,model_name+"."+ self.model_name())
        f = open(path, 'wb')
        cPickle.dump(self.model, f, 2)
        f.close()
        print "--- Save done in {} seconds\n".format(time()-started)

    
    def load_model(self,model_name):
        print "--- Loading model {}".format(model_name)
        started = time()
        path = os.path.join(self.work_path,model_name)
        f = open(path, 'rb')
        tmp_dict = cPickle.load(f)
        f.close()
        print "--- Load done in {} seconds\n".format(time()-started)
        self.model = tmp_dict 
        return tmp_dict 


    def model_name(self):
        name = self.model.__class__.__name__
        #print name
        return name



    def make_img_predictble(self, img_path):
        img = imread(img_path)
        img_resized = resize(img, self.im_dim, anti_aliasing=True, mode='reflect')
        return img_resized







    def predict(self, img):
        
        lbl = self.model.predict(img)
        print lbl
        return lbl
    
    
    def predict_all_path(self, path):
        
        if not os.path.isdir(path):
            print "--- Path not a directory ---\n"
            return -1

        files = os.listdir(path)
        flat_data = []
        for file in files:
            img = imread(os.path.join(path,file))
            img = resize(img, self.im_dim, anti_aliasing=True, mode='reflect')
            img = np.array(img.flatten()).reshape(1,-1)
            print file, '---->',self.categories[self.model.predict(img)[0]]
            
            flat_data.append(img.flatten()) 
        
        flat_data = np.array(flat_data)

        print self.model.predict(flat_data)

    
    
    
    
    
        
def main():

    #dp = Data_process("Activities/as")
    #image_dataset = load_image_files(dp.work_path+"/Images")
    #return 
    #print brunch['target_names']
    #brunch['target_names'].sort()
    #print brunch['target_names']
    tk = My_toolkit("Activities/as")

    tk.load_database()
    #tk.svm_model()
    tk.knn_model(1)
    
    print tk.database
    # print tk.y_train
    # return 
    # tk.model_name()
    
    # tk.mlp_model()
    # tk.model_name()

    # tk.nayve_model()
    # tk.model_name()

    tk.fit_model()
    tk.save_model("1NN")
    
    #tk.model = tk.load_model("try.SVC")
    
    path = tk.work_path+"/test"
    
    
    print path
    tk.predict_all_path(path)

    tk.evaluate()


    return



    # nei = [1,3,5,7]
    # for i in nei:
    #     tk.knn_model(i)
    #     tk.fit_model()
    #     tk.evaluate()
    #     tk.save_model(tk.model,str(i),"knn")
        
    # tk.save()

    #tk.model = tk.load_model("first","svm")

    #print tk.model


    print "THE END!"
    return
    










    '''
    X_train, X_test, y_train, y_test = train_test_split(
    image_dataset.data, image_dataset.target, test_size=0.3,random_state=109)

    # print y_test

    param_grid = [
    {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
    {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
    ]
    svc = svm.SVC()
    clf = GridSearchCV(svc, param_grid)
    clf.fit(X_train, y_train)    
    '''
























def load_image_files( container_path, dimension):
    """
    Load image files with categories as subfolder names 
    which performs like scikit-learn sample dataset
    
    Parameters
    ----------
    container_path : string or unicode
        Path to the main folder holding one subfolder per category
    dimension : tuple
        size to which image are adjusted to
        
    Returns
    -------
    Bunch
    """
    image_dir = Path(container_path)
    folders = [directory for directory in image_dir.iterdir() if directory.is_dir()]
    # print folders
    folders.sort()
    # print folders
    # return 

    categories = [fo.name for fo in folders]
    descr = "A image classification dataset"
    images = []
    flat_data = []
    target = []
    for i, direc in enumerate(folders):
        for file in direc.iterdir():
            img = imread(file)
            img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
            flat_data.append(img_resized.flatten()) 
            images.append(img_resized)
            target.append(i)
    flat_data = np.array(flat_data)
    target = np.array(target)
    images = np.array(images)

    return Bunch(data=flat_data,
                 target=target,
                 target_names=categories,
                 images=images,
                 DESCR=descr)






if __name__=="__main__":
    main()
