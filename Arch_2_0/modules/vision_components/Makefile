img = 
db = DBIM/alldb
classifier = mlp

mlp:
	python mlp.py --dataset $(db)

knn:
	python knn.py --dataset $(db)

svm:
	python svm.py --dataset $(db)

classify:
ifeq ($(img),)
	@echo usage: make classify img=x, where inputs/x.jpg
else
	python $(classifier).py --dataset $(db) -c inputs/$(img).jpg
endif
