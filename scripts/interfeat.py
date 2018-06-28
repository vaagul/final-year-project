from spacy.lang.en import English

def get_questions_matrix_sum(questions, nlp,c_id,q1):
	
	assert not isinstance(questions, basestring)
	nb_samples = len(questions)
	word_vec_dim = nlp(questions[0])[0].vector.shape[0]
	questions_matrix = np.zeros((nb_samples, word_vec_dim))
	word_vec(c_id,q1)
	for i in xrange(len(questions)):
		tokens = nlp(questions[i])
		for j in xrange(len(tokens)):
			questions_matrix[i,:] += tokens[j].vector
		print question_matrix[i,:]
	return



def main():
	nlp = English()
	ques = open('../data/preprocessed/questions_val2014.txt', 'r').read().decode('utf8').splitlines()
	for i, q in zip(xrange(len(ques)),ques):	
		get_questions_matrix_sum(q,nlp," "," ")
		print "123"




