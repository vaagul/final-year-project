import operator
import argparse
import progressbar
import json
from spacy.lang.en import English

def getModalAnswer(answers):
	candidates = {}
	for i in xrange(10):
		candidates[answers[i]['answer']] = 1

	for i in xrange(10):
		candidates[answers[i]['answer']] += 1

	return max(candidates.iteritems(), key=operator.itemgetter(1))[0]

def getAllAnswer(answers):
	answer_list = []
	for i in xrange(10):
		answer_list.append(answers[i]['answer'])

	return ';'.join(answer_list)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-split', type=str, default='train', 
		help='')
	parser.add_argument('-answers', type=str, default='modal',
		help='')
	args = parser.parse_args()

	nlp = English()

	if args.split == 'train':
		annFile = '../data/mscoco_train2014_annotations.json'
		quesFile = '../data/OpenEnded_mscoco_train2014_questions.json'
		questions_file = open('../data/preprocessed/questions_train2014.txt', 'w')
		questions_id_file = open('../data/preprocessed/questions_id_train2014.txt', 'w')
		questions_lengths_file = open('../data/preprocessed/questions_lengths_train2014.txt', 'w')
		if args.answers == 'modal':
			answers_file = open('../data/preprocessed/answers_train2014_modal.txt', 'w')
		elif args.answers == 'all':
			answers_file = open('../data/preprocessed/answers_train2014_all.txt', 'w')
		coco_image_id = open('../data/preprocessed/images_train2014.txt', 'w')
		data_split = 'training data'
	elif args.split == 'val':
		annFile = '../data/mscoco_val2014_annotations.json'
		quesFile = '../data/OpenEnded_mscoco_val2014_questions.json'
		questions_file = open('../data/preprocessed/questions_val2014.txt', 'w')
		questions_id_file = open('../data/preprocessed/questions_id_val2014.txt', 'w')
		questions_lengths_file = open('../data/preprocessed/questions_lengths_val2014.txt', 'w')
		if args.answers == 'modal':
			answers_file = open('../data/preprocessed/answers_val2014_modal.txt', 'w')
		elif args.answers == 'all':
			answers_file = open('../data/preprocessed/answers_val2014_all.txt', 'w')
		coco_image_id = open('../data/preprocessed/images_val2014_all.txt', 'w')
		data_split = 'validation data'
	else:
		raise RuntimeError('Incorrect split. Your choices are:\ntrain\nval\ntest-dev\ntest')

	
	questions = json.load(open(quesFile, 'r'))
	ques = questions['questions']
	if args.split == 'train' or args.split == 'val':
		qa = json.load(open(annFile, 'r'))
		qa = qa['annotations']
	
	pbar = progressbar.ProgressBar()
	print 'Dumping questions, answers, questionIDs, imageIDs, and questions lengths to text files...'
	for i, q in pbar(zip(xrange(len(ques)),ques)):
		questions_file.write((q['question'] + '\n').encode('utf8'))
		questions_lengths_file.write((str(len(nlp(q['question'])))+ '\n').encode('utf8'))
		questions_id_file.write((str(q['question_id']) + '\n').encode('utf8'))
		coco_image_id.write((str(q['image_id']) + '\n').encode('utf8'))
		if args.split == 'train' or args.split == 'val':
			if args.answers == 'modal':
				answers_file.write(getModalAnswer(qa[i]['answers']).encode('utf8'))
			elif args.answers == 'all':
				answers_file.write(getAllAnswer(qa[i]['answers']).encode('utf8'))
			answers_file.write('\n'.encode('utf8'))

	print 'completed dumping', data_split

if __name__ == "__main__":
	main()
