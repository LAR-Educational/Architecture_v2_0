#from vision_components.classifiers import svm, knn, mlp

import sys
import numpy as np
import vars
from naoqi import ALProxy
import vision_definitions
import cv2


import time



# subscribe top camera
AL_kTopCamera = 0
AL_kQVGA = 1            # 320x240
AL_kBGRColorSpace = 13





def subscribe():
    
    nameId = vars.camera.subscribeCamera("Tozadore", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)
    print "Subscribed in ", nameId
    return nameId


def see():
    
    subId = subscribe()   
    
    result = vars.camera.getImageRemote(subId)
   
   # create image
    width = result[0]
    height = result[1]
    image = np.zeros((height, width, 3), np.uint8)
    
    key=0    
    
    #while key!=27:
        
    # get image
    result = vars.camera.getImageRemote(subId)
    
    if result == None:
        print 'cannot capture.'
    elif result[6] == None:
        print 'no image data string.'
    else:
    
        # translate value to mat
        values = map(ord, list(result[6]))
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image.itemset((y, x, 0), values[i + 0])
                image.itemset((y, x, 1), values[i + 1])
                image.itemset((y, x, 2), values[i + 2])
                i += 3
                
        # show image
        #cv2.imshow("NAO's Vision top-camera-320x240", image)
            
        # exit by [ESC]
                
        #key=cv2.waitKey(1)        
        #        if cv2.waitKey(1) == 27:
        #            break
        #        
    
    unsub(subId)
    return image

    
def unsub(subId):
        vars.camera.unsubscribe(subId)











'''
def initializate(data_training_path, classifier='all'):
    
    try:
        if(classifier == 'knn'):
            knn.initializate(data_training_path)
            knn.fit()
        elif(classifier == 'mlp'):
            mlp.initializate(data_training_path)
            mlp.fit()
        elif(classifier == 'svm'):
            svm.initializate(data_training_path)
            svm.fit()
        elif(classifier == 'all'):
            
            knn.initializate(data_training_path)
            mlp.initializate(data_training_path)
            svm.initializate(data_training_path)
            start_time = time.time()
            knn.fit()
            print("KNN trainning time: %s seconds " % (time.time() - start_time))            
            
            start_time = time.time()
            mlp.fit()
            print("MLP trainning time: %s seconds " % (time.time() - start_time))            
            
            start_time = time.time()
            svm.fit()
            print("SVM trainning time: %s seconds " % (time.time() - start_time))            

        vars.info("Vision system Online.")
        vars.info("Using classifier type: " + vars.classifierType)
    
    except:
        vars.info("Vision System Exception: " +  str(sys.exc_info()[0]))
       
 

def classify(img_path, classifier='all', imshow=False):
    
    if(classifier == 'knn'):
        return knn.classify(img_path)
    elif(classifier == 'mlp'):
        return mlp.classify(img_path)
    elif(classifier == 'svm'):
        return svm.classify(img_path)
    elif(classifier == 'all'):
        knn_ret = knn.classify(img_path, imshow)
        mlp_ret = mlp.classify(img_path, imshow)
        svm_ret = svm.classify(img_path, imshow)
        #print '--------------------------------------DEBUG----------------------------------------------'


        # isso pode ser substituido por moda

        votes_hst = np.array([0, 0, 0])
        votes_hst[int(knn_ret['hst']['label'])] +=  1
        votes_hst[int(mlp_ret['hst']['label'])] +=  1
        votes_hst[int(svm_ret['hst']['label'])] +=  1

        label = -1
        
        if(votes_hst[0] > votes_hst[1] and votes_hst[0] > votes_hst[2]):
            label = 0
        if(votes_hst[1] > votes_hst[0] and votes_hst[1] > votes_hst[2]):
            label = 1
        if(votes_hst[2] > votes_hst[0] and votes_hst[2] > votes_hst[1]):
            label = 2

        hst_c = {'label':label, '0':(votes_hst[0]/3.0) ,'1':(votes_hst[1]/3.0), '2': (votes_hst[2]/3.0), '-1': (votes_hst[2]/3.0) }



        votes_pxl = np.array([0, 0, 0])
        votes_pxl[int(knn_ret['pxl']['label'])] +=  1
        votes_pxl[int(mlp_ret['pxl']['label'])] +=  1
        votes_pxl[int(svm_ret['pxl']['label'])] +=  1

        label = -1
        
        if(votes_pxl[0] > votes_pxl[1] and votes_pxl[0] > votes_pxl[2]):
            label = 0
        if(votes_pxl[1] > votes_pxl[0] and votes_pxl[1] > votes_pxl[2]):
            label = 1
        if(votes_pxl[2] > votes_pxl[0] and votes_pxl[2] > votes_pxl[1]):
            label = 2


        pxl_c = {'label':label, '0': (votes_pxl[0]/3.0) ,'1':(votes_pxl[1]/3.0), '2': (votes_pxl[2]/3.0), '-1': (votes_pxl[2]/3.0)  }
        



        votes_all = votes_hst+votes_pxl 
        label = -1

        if(votes_all[0] > votes_all[1] and votes_all[0] > votes_all[2]):
            label = 0
        if(votes_all[1] > votes_all[0] and votes_all[1] > votes_all[2]):
            label = 1
        if(votes_all[2] > votes_all[0] and votes_all[2] > votes_all[1]):
            label = 2

        all_c = {'label':label, '0':(votes_all[0]/6.0) ,'1':(votes_all[1]/6.0), '2': (votes_all[2]/6.0), '-1': (votes_all[2]/6.0)  }

        write_csv = {'class':'none',
                     'knn_hst': str(knn_ret['hst']['label']) + '_' + str(knn_ret['hst'][str(knn_ret['hst']['label'])]),
                     'knn_pxl': str(knn_ret['pxl']['label']) + '_' + str(knn_ret['pxl'][str(knn_ret['pxl']['label'])]), 
                     'mlp_hst': str(mlp_ret['hst']['label']) + '_' + str(mlp_ret['hst'][str(mlp_ret['hst']['label'])]), 
                     'mlp_pxl': str(mlp_ret['pxl']['label']) + '_' + str(mlp_ret['pxl'][str(mlp_ret['pxl']['label'])]), 
                     'svm_hst': str(svm_ret['hst']['label']) + '_' + str(svm_ret['hst'][str(svm_ret['hst']['label'])]), 
                     'svm_pxl': str(svm_ret['pxl']['label']) + '_' + str(svm_ret['pxl'][str(svm_ret['pxl']['label'])]), 
                     'ensemble_hst': str(hst_c['label']) + '_' + str(hst_c[str(hst_c['label'])]), 
                     'ensemble_pxl': str(pxl_c['label']) + '_' + str(pxl_c[str(pxl_c['label'])]), 
                     'ensemble_all': str(all_c['label']) + '_' + str(all_c[str(all_c['label'])])}

        print 'TESTE AALL', all_c
        return {'pxl':pxl_c, 'hst':hst_c, 'all':all_c, 'csv':write_csv}



def print_proba(ret, classifier='knn', full=False):
    if(classifier == 'knn'):
        knn.print_proba(ret, full)
    elif(classifier == 'mlp'):
        mlp.print_proba(ret, full)
    elif(classifier == 'svm'):
        svm.print_proba(ret, full)
    elif(classifier == 'all'):
        print("HST")
        print("Label: " + str(ret['hst']['label']))
        print("0: " + str(ret['hst']['0']))
        print("1: " + str(ret['hst']['1']))
        print("2: " + str(ret['hst']['2']))
        print("\nPXL")
        print("Label: " + str(ret['pxl']['label']))
        print("0: " + str(ret['pxl']['0']))
        print("1: " + str(ret['pxl']['1']))
        print("2: " + str(ret['pxl']['2']))
        print("\nALL    ")
        print("Label: " + str(ret['all']['label']))
        print("0: " + str(ret['all']['0']))
        print("1: " + str(ret['all']['1']))
        print("2: " + str(ret['all']['2']))
        print("")
'''        
