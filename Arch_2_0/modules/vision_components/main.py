# -*- coding: utf-8 -*-

import vision
import numpy as np
import matplotlib.pyplot as plt


import time

default = 'mlp'

def main():
	vision.initializate(classifier = default)

	# ...


	img_path = 'inputs/0/0.jpg'
	
	ret = vision.classify(img_path, classifier = default)
	
	vision.print_proba(ret, classifier = default)


	# begin = time.time()
	# knn.fit()
	# end = time.time()
	# print("Tempo de treinamento KNN: " +  str(end-begin))
	
	# begin = time.time()
	# mlp.fit()
	# end = time.time()
	# print("Tempo de treinamento MLP: " +  str(end-begin))
	
	# begin = time.time()
	# svm.fit()
	# end = time.time()
	# print("Tempo de treinamento SVM: " +  str(end-begin))


	# knn_ret = knn.classify(img_path)
	# mlp_ret = mlp.classify(img_path)
	# svm_ret = svm.classify(img_path)

	# knn.print_proba(knn_ret, full=False)	
	# mlp.print_proba(mlp_ret, full=False)	
	# svm.print_proba(svm_ret, full=False)	



	#Retorno:
		# O retorno da função é um dicionário contendo dois valores: 'pxl' e 'hst',
		# que indica os resultados de cada método.
		# 'pxl' e 'hst' também é um dicionário, contendo os seguintes valores:
		# {'label':label da imagem, '0':prob de ser 0 ,'1':prob de ser 1, '2': prob de ser 2 }


	# n_groups = 3

	# means_pxlknn = (knn_ret['pxl']['0'], knn_ret['pxl']['1'], knn_ret['pxl']['2'])
	# std_zero = (0, 0, 0)

	# means_hstknn = (knn_ret['hst']['0'], knn_ret['hst']['1'], knn_ret['hst']['2'])

	# means_pxlmlp = (mlp_ret['pxl']['0'], mlp_ret['pxl']['1'], mlp_ret['pxl']['2'])

	# means_hstmlp = (mlp_ret['hst']['0'], mlp_ret['hst']['1'], mlp_ret['hst']['2'])

	# means_pxlsvm = (svm_ret['pxl']['0'], svm_ret['pxl']['1'], svm_ret['pxl']['2'])

	# means_hstsvm = (svm_ret['hst']['0'], svm_ret['hst']['1'], svm_ret['hst']['2'])

	# fig, ax = plt.subplots()

	# index = np.arange(n_groups)
	# bar_width = 0.15

	# opacity = 0.4
	# error_config = {'ecolor': '0.3'}

	# rects1 = plt.bar(index, means_hstknn, bar_width,
	#                  alpha=opacity,
	#                  color='b',
	#                  yerr=std_zero,
	#                  error_kw=error_config,
	#                  label='KNN_HST')

	# rects2 = plt.bar(index + bar_width, means_pxlknn, bar_width,
	#                  alpha=opacity,
	#                  color='b',
	#                  yerr=std_zero,
	#                  error_kw=error_config,
	#                  label='KNN_PXL')

	# rects3 = plt.bar(index + bar_width, means_hstsvm, bar_width,
	#                  alpha=opacity,
	#                  color='r',
	#                  yerr=std_zero,
	#                  error_kw=error_config,
	#                  label='SVM_HST')

	# rects4 = plt.bar(index + bar_width, means_pxlsvm, bar_width,
	#                  alpha=opacity,
	#                  color='r',
	#                  yerr=std_zero,
	#                  error_kw=error_config,
	#                  label='PXL_HST')

	# rects5 = plt.bar(index + bar_width, means_hstmlp, bar_width,
	#                  alpha=opacity,
	#                  color='g',
	#                  yerr=std_zero,
	#                  error_kw=error_config,
	#                  label='MLP_HST')

	# rects6 = plt.bar(index + bar_width, means_pxlmlp, bar_width,
	#                  alpha=opacity,
	#                  color='g',
	#                  yerr=std_zero,
	#                  error_kw=error_config,
	#                  label='PXL_MLP')



	# plt.xlabel('Label')
	# plt.ylabel('Prob')
	# plt.title('prob x label')
	# plt.xticks(index + bar_width / 2, ('0', '1', '2'))
	# plt.legend()

	# plt.tight_layout()
	# plt.show()

if __name__ == "__main__":
	main()