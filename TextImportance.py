# -*- coding: utf-8 -*-
# @Date    : 2018-05-17 15:55:36
# @Author  : Liu Huan (liuhuan@mail.las.ac.cn)

import nltk
import os
import numpy as np
import sys
import jieba

with open('stopwords.txt', 'r', encoding='utf-8') as f:
    stoplist = [line.strip() for line in f.readlines()]


def is_chinese(char):
    if char >= '\u4e00' and char <= '\u9fa5':
        return True
    else:
        return False


def is_alphabet(char):
    if (char >= '\u0041' and char <= '\u005a') or (char >= '\u0061' and char <= '\u007a'):
        return True
    else:
        return False


def preprocessing(sen):
    word_list = ' '.join(jieba.cut(sen)).split(' ')
    final_sen = []
    for word in word_list:
        if word != '':
            flag = 0
            if is_chinese(word[0]):
                flag = 1
            if is_alphabet(word[0]):
                flag = 2  # 如果是英文，则进行词干提取
                s = nltk.stem.SnowballStemmer('english')
                word = s.stem(word)
            if flag != 0:
                if word not in stoplist:
                    final_sen.append(word)
    return final_sen


def readfiles(docs_path, new_text_path):
    docs = []
    for filename in os.listdir(docs_path):
        file = os.path.join(docs_path, filename)
        with open(file, 'r', encoding='gb18030', errors='ignore') as f:
            sens = [line.strip() for line in f. readlines()]
        docs.append(' '.join(sens))
    # print(docs[0])
    with open(new_text_path, 'r', encoding='gb18030', errors='ignore') as f:
        sen = ' '.join([line.strip() for line in f. readlines()])
    docs.append(sen)  # 将新文档加入文档集
    return docs


def tfidf(docs):
    corpus = []
    for doc in docs:
        corpus.append(preprocessing(doc))
    keywords = []  # 构建词典
    for cor in corpus:
        for word in cor:
            if word not in keywords:
                keywords.append(word)
    # 计算TF
    TF = np.zeros([len(corpus), len(keywords)])
    for i in range(len(corpus)):
        j = 0
        for word in keywords:
            TF[i, j] = corpus[i].count(word)
            # tf_dict[word] += TF[i, j]
            j += 1
    # 计算DF
    DF = np.zeros([1, len(keywords)])
    for i in range(len(keywords)):
        for cor in corpus:
            if keywords[i] in cor:
                DF[0, i] += 1
        DF[0, i] += 1  # 加1防止出现0
 # 计算IDF
    IDF = np.log(len(corpus)/DF)
    # 计算TFIDF
    TFIDF = TF*IDF
    return TFIDF


def cosine(Vec1, Vec2):
    return np.dot(Vec1, Vec2)/(np.linalg.norm(Vec1)*(np.linalg.norm(Vec2)))


def euclidean(Vec1, Vec2):
    return np.linalg.norm(Vec1 - Vec2)


if __name__ == '__main__':
    docs_path = sys.argv[1]
    new_text_path = sys.argv[2]
    # docs_path = r'D:\UCAS\Phd\Projects\201805YuGaiHong\上科大项目机器学习文档'
    # new_text_path = r'D:\UCAS\Phd\Projects\201805YuGaiHong\new1.txt'
    docs = readfiles(docs_path, new_text_path)
    TFIDF = tfidf(docs)
    score = 0
    for i in range(len(docs)-1):
        score += cosine(TFIDF[i], TFIDF[-1])
    print(score/(len(docs)-1))
