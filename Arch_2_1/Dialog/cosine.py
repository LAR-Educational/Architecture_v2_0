from sklearn.feature_extraction.text import TfidfVectorizer


def cosine():
	with open('all_questions.textile') as f:
        	questions_all = f.read().splitlines() 
        	f.close();

	with open('questions.textile') as f:
     		questions = f.read().splitlines() 
        	f.close()


	print ("Choose the index to be compared (iguals index must result in the most similar rate)")

	index_all = raw_input("index one: ")
	index_word = raw_input("index two: ")
	
	full_question = questions_all[int(index_all)]
	question = questions[int(index_word)]
	
	print full_question
	print question
	documents = (full_question, question)
	
	tfidf_vectorizer = TfidfVectorizer()
	tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
	
	from sklearn.metrics.pairwise import cosine_similarity
	return (cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)[0,1])