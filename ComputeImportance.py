# -*- coding: utf-8 -*-
# @Date    : 2018-05-17 15:55:36
# @Author  : Liu Huan (liuhuan@mail.las.ac.cn)

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import numpy as np
import sys

def preprocessing(sen):
	word_list=word_tokenize(text=sen,language="english")#分词
	s = nltk.stem.SnowballStemmer('english') 
	final_sen=[]
	for word in word_list:
		if word.isalpha():#过滤数字，标点
			word=s.stem(word)#提取词干
			if word not in stopwords.words('english'):#去除停用词
				final_sen.append(word)
	return final_sen

def  readfiles(docs_path,new_text_path):
	docs=[]
	for filename in os.listdir(docs_path):
		file=os.path.join(docs_path,filename)
		with open(file,'r',encoding='gb18030',errors='ignore') as f:
			sens=[line.strip() for line in f. readlines()]
		docs.append(' '.join(sens))
	# print(docs[0])
	with open(new_text_path,'r',encoding='gb18030',errors='ignore') as f:
		sen=' '.join([line.strip() for line in f. readlines()])
	docs.append(sen)#将新文档加入文档集
	return docs

def tfidf(docs):
	corpus=[]
	for doc in docs:
		corpus.append(preprocessing(doc))
	keywords=[]#构建词典
	for cor in corpus:
		for word in cor:
			if word not in keywords:
				keywords.append(word)
	# print(len(keywords))
	# print(keywords)
	#计算tf
	TF=np.zeros([len(corpus),len(keywords)])
	# print(TF.shape)
	for i in range(len(corpus)):
		j=0
		for word in keywords:
			# print(word)
			TF[i,j]=corpus[i].count(word)
			# print('[',str(i),',',str(j),']')
			# print(TF[i,j])
			j+=1
	# print(TF.shape)
	#计算IDF
	IDF=np.zeros([1,len(keywords)])
	for i in range(len(keywords)):
		for cor in corpus:
			if keywords[i] in cor:
				IDF[0,i]+=1
		IDF[0,i]+=1#加1防止出现0
	IDF=np.log(len(corpus)/IDF)
	#计算TFIDF
	TFIDF=TF*IDF
	return TFIDF

def cosine(Vec1,Vec2):
	return np.dot(Vec1,Vec2)/(np.linalg.norm(Vec1)*(np.linalg.norm(Vec2)))  

def  euclidean(Vec1,Vec2):
	return np.linalg.norm(Vec1 - Vec2) 


if __name__ == '__main__':
	# print('hahahah')
	docs_path=sys.argv[1]
	new_text_path=sys.argv[2]
	# print(docs_path,new_text_path)
	docs=readfiles(docs_path,new_text_path)
	TFIDF=tfidf(docs)
	# score=0
	# for i in range(len(docs)-1):
	# 	score+=euclidean(TFIDF[i],TFIDF[-1])
	# print(1-(score/(len(docs)-1)))
	score=0
	for i in range(len(docs)-1):
		score+=cosine(TFIDF[i],TFIDF[-1])
	print(score/(len(docs)-1))
