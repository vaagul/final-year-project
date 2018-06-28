import re, math
from collections import Counter

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text,WORD):
     words = WORD.findall(text)
     return Counter(words)

def cosine(text1,text2):
	WORD = re.compile(r'\w+')
	vector1 = text_to_vector(text1,WORD)
	vector2 = text_to_vector(text2,WORD)
	cosine = get_cosine(vector1, vector2)
	#print 'Cosine:', cosine
	return cosine

def word_vec(image_id,question_id):
	if(image_id==" " or question_id== " "):
		return
	questions_val = open('../data/preprocessed/questions_val2014.txt', 
							'r').read().decode('utf8').splitlines()
	answers_val = open('../data/preprocessed/answers_val2014_all.txt', 
							'r').read().decode('utf8').splitlines()
	images_val = open('../data/preprocessed/images_val2014_all.txt', 
							'r').read().decode('utf8').splitlines()
	truth1="no"
	for truth, question, image in zip(answers_val, questions_val, images_val):
			flag=0
			if(cosine(question,question_id)>0.5 and image_id==image):
				truth1=truth.split(';')
				flag=1
				break
	if(flag==1):
		print truth1[0]
	else:
		print "yes"



