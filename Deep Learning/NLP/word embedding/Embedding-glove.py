#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created on 2020/4/24 10:25
Update  on 2020/4/24 10:25
Author: 不告诉你
Software: PyCharm
GitHub: https://github.com/Saber891
"""
import os
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import numpy as np

imdb_dir = '../../../imdb-data/aclImdb'

train_dir = os.path.join(imdb_dir, 'train')

labels = []
texts = []

for label_type in ['neg', 'pos']:
    dir_name = os.path.join(train_dir, label_type)
    for fname in os.listdir(dir_name):
        if fname[-4:] == '.txt':
            f = open(os.path.join(dir_name, fname), encoding='utf-8')
            texts.append(f.read())
            f.close()
            if label_type == 'neg':
                labels.append(1)
            else:
                labels.append(0)

maxlen = 100  # 在 100 个单词后截断评论
tarining_samples = 200  # 在 200 个样本上训练
validation_samples = 10000  # 在 10 000 个样本上验证
max_words = 10000  # 只考虑数据集中前 10 000 个最常见的单词

tokenizer = Tokenizer(num_words=max_words)  # 用来对文本中的词进行统计计数，生成文档词典，以支持基于词典位序生成文本的向量表示
tokenizer.fit_on_texts(texts)  # 使用一系列文档来生成 token 词典，texts 为 list 类，每个元素为一个文档
sequences = tokenizer.texts_to_sequences(texts)  # ) 将多个文档转换为 word 下标的向量形式

word_index = tokenizer.word_index  # 一个 dict，保存所有 word 对应的编号 id，从 1 开始
print('Found %s unique tokens .' % len(word_index))

data = pad_sequences(sequences, maxlen=maxlen)  # 将多个序列截断或补齐为相同长度

labels = np.asanyarray(labels)
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)
print('Shape of data[0]', data.shape[0])

indices = np.arange(data.shape[0])  # 将数据划分为训练集和验证集，但首先要打乱数据，因为一开始数据中的样本是排好序的（所有负面评论都在前面，然后是所有正面评论）
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]

x_train = data[:tarining_samples]
y_train = labels[:tarining_samples]
x_val = data[tarining_samples:tarining_samples + validation_samples]
y_val = labels[tarining_samples:tarining_samples + validation_samples]

glove_dir = '../../../imdb-data/glove.6B/'
embeddings_index = {}
f = open(os.path.join(glove_dir, 'glove.6B.100d.txt'))
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asanyarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()
print('Found %s word vector.' %len(embeddings_index))

