import csv
import time

fieldnames = ['class', 'knn_hst', 'knn_pxl', 'mlp_hst', 'mlp_pxl', 'svm_hst', 'svm_pxl', 'ensemble_hst', 'ensemble_pxl', 'ensemble_all']
writer = None
# path = 'results/vision_results/'
path = '../../results/vision_results/'
file = 'results_' + str(time.ctime()) +'.csv' 

def initializate(fname=file):
	global writer
	global file
	file = fname
	with open(path+file, 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

def write_row(values):
	global writer
	with open(path+file, 'a') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writerow({ fieldnames[0]: values['class'],
						  fieldnames[1]: values['knn_hst'],
						  fieldnames[2]: values['knn_pxl'],
						  fieldnames[3]: values['mlp_hst'],
						  fieldnames[4]: values['mlp_pxl'],
						  fieldnames[5]: values['svm_hst'],
						  fieldnames[6]: values['svm_pxl'],
						  fieldnames[7]: values['ensemble_hst'],
						  fieldnames[8]: values['ensemble_pxl'],
						  fieldnames[9]: values['ensemble_all']})


def process(fname):
	hit = [0,0,0,0,0,0,0,0,0,0]
	label_0 = [0,0,0,0,0,0,0,0,0,0]
	label_1 = [0,0,0,0,0,0,0,0,0,0]
	label_2 = [0,0,0,0,0,0,0,0,0,0]

	with open(path+fname) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			# print(row[fieldnames[0]], row[fieldnames[1]].split('_')[0],
			# 	  row[fieldnames[2]].split('_')[0], row[fieldnames[3]].split('_')[0],
			# 	  row[fieldnames[4]].split('_')[0], row[fieldnames[5]].split('_')[0],
			# 	  row[fieldnames[6]].split('_')[0], row[fieldnames[7]].split('_')[0],
			# 	  row[fieldnames[8]].split('_')[0], row[fieldnames[9]].split('_')[0])

			# hit[0] - contador de testes
			for i in range(0,10):
				if(row[fieldnames[0]] == row[fieldnames[i]].split('_')[0]):
					hit[i] += 1
					if(row[fieldnames[0]] == '0'):
						label_0[i] += 1
					if(row[fieldnames[0]] == '1'):
						label_1[i] += 1
					if(row[fieldnames[0]] == '2'):
						label_2[i] += 1

		for i in range(1,10):
			print("Classificador: " + fieldnames[i])
			print("\tNumero de acertos por classes:")
			print("\t0: " + str(label_0[i]/float(label_0[0])) + "\t1: " + str(label_1[i]/float(label_1[0]))  + "\t2: " + str(label_2[i]/float(label_2[0])) )
			print("\tPorcentagem de acertos total: " + str(hit[i]/float(hit[0])))
			print("")
 

def main():	
	process('results_Thu May 18 17:24:49 2017.csv')
	# initializate()
	#write_row('e', '1', '2', '0', '1', '2', '0', '1', '0', '2')

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