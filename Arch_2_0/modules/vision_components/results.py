import csv
import time

fieldnames = ['class', 'knn_hst', 'hst_pxl', 'mlp_hst', 'mlp_pxl', 'svm_hst', 'svm_pxl', 'ensemble_hst', 'ensemble_pxl', 'ensemble_all']
writer = None
file = 'results_' + str(time.ctime()) +'.csv' 

def initializate(fname=file):
	global writer
	global file
	file = fname
	with open(fname, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

def write_row(label, knn_hst, hst_pxl, mlp_hst, mlp_pxl, svm_hst, svm_pxl, ensemble_hst, ensemble_pxl, ensemble_all):
	global writer
	with open(file, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writerow({ fieldnames[0]: label,
						  fieldnames[1]: knn_hst,
						  fieldnames[2]: hst_pxl,
						  fieldnames[3]: mlp_hst,
						  fieldnames[4]: mlp_pxl,
						  fieldnames[5]: svm_hst,
						  fieldnames[6]: svm_pxl,
						  fieldnames[7]: ensemble_hst,
						  fieldnames[8]: ensemble_pxl,
						  fieldnames[9]: ensemble_all})


def main():
	initializate()
	write_row('e', '1', '2', '0', '1', '2', '0', '1', '0', '2')


        # write_csv = {'class':'none',
        #              'knn_hst': str(knn_ret['hst']['label']) + '_' + str(knn_ret['hst'][str(knn_ret['hst']['label'])]),
        #              'hst_pxl': str(knn_ret['pxl']['label']) + '_' + str(knn_ret['pxl'][str(knn_ret['pxl']['label'])]), 
        #              'mlp_hst': str(mlp_ret['hst']['label']) + '_' + str(mlp_ret['hst'][str(mlp_ret['hst']['label'])]), 
        #              'mlp_pxl': str(mlp_ret['pxl']['label']) + '_' + str(mlp_ret['pxl'][str(mlp_ret['pxl']['label'])]), 
        #              'svm_hst': str(svm_ret['hst']['label']) + '_' + str(svm_ret['hst'][str(svm_ret['hst']['label'])]), 
        #              'svm_pxl': str(svm_ret['pxl']['label']) + '_' + str(svm_ret['pxl'][str(svm_ret['pxl']['label'])]), 
        #              'ensemble_hst': str(hst_c['label']) + '_' + str(hst_c[str(hst_c['label'])]), 
        #              'ensemble_pxl': str(pxl_c['label']) + '_' + str(pxl_c[str(pxl_c['label'])]), 
        #              'ensemble_all': str(all_c['label']) + '_' + str(all_c[str(all_c['label'])])}



if __name__ == "__main__":
	main()