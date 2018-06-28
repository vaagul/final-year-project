import numpy as np
from argmodel import word_vec
from keras.utils import np_utils


def get_questions_tensor_timeseries(questions, nlp, timesteps):
	
	assert not isinstance(questions, basestring)
	nb_samples = len(questions)
	word_vec_dim = nlp(questions[0])[0].vector.shape[0]
	questions_tensor = np.zeros((nb_samples, timesteps, word_vec_dim))
	for i in xrange(len(questions)):
		tokens = nlp(questions[i])
		for j in xrange(len(tokens)):
			if j<timesteps:
				questions_tensor[i,j,:] = tokens[j].vector

	return questions_tensor

def get_questions_matrix_sum(questions, nlp):
	
	assert not isinstance(questions, basestring)
	nb_samples = len(questions)
	word_vec_dim = nlp(questions[0])[0].vector.shape[0]
	questions_matrix = np.zeros((nb_samples, word_vec_dim))
	#word_vec(c_id,q1)
	for i in xrange(len(questions)):
		tokens = nlp(questions[i])
		for j in xrange(len(tokens)):
			questions_matrix[i,:] += tokens[j].vector
	return questions_matrix

def get_answers_matrix(answers, encoder):
	
	assert not isinstance(answers, basestring)
	y = encoder.transform(answers) #string to numerical class
	nb_classes = encoder.classes_.shape[0]
	Y = np_utils.to_categorical(y, nb_classes)
	return Y

def get_images_matrix(img_coco_ids, img_map, VGGfeatures):
	
	assert not isinstance(img_coco_ids, basestring)
	nb_samples = len(img_coco_ids)
	nb_dimensions = VGGfeatures.shape[0]
	image_matrix = np.zeros((nb_samples, nb_dimensions))
	for j in xrange(len(img_coco_ids)):
		image_matrix[j,:] = VGGfeatures[:,img_map[img_coco_ids[j]]]

	return image_matrix
