#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from scipy import spatial

import numpy as np

from collections import Counter
import string
import math

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize
import sys
import crawl

sys.setrecursionlimit(4000)

# In[4]:


df = pd.read_csv("/Users/admin/PycharmProjects/cw_ir/pub.csv", index_col=False)


# In[20]:


def basic_preprocess_case(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def del_stop_words_stemming(text):
    pstemmer = PorterStemmer()
    stop_words = stopwords.words('english')
    text1 = ""
    for word in word_tokenize(text):
        if word not in stop_words and len(word) > 1:
            text1 = text1 + " " + word
        text1 = text1 + " " + pstemmer.stem(word)

    return text1


# In[21]:


def preprocess(text):
    text = basic_preprocess_case(text)
    text = del_stop_words_stemming(text)
    return text


# In[22]:


processed_text = []

for index, item in df.iterrows():
    text = item["pub_title"] + " " + item["auth_name_extract"] + " " + item["pub_date"]
    processed_text.append(word_tokenize(str(preprocess(text))))

# In[23]:


date_freq = {}
for i in range(len(processed_text)):
    tokens = processed_text[i]
    for w in tokens:
        try:
            date_freq[w].add(i)
        except:
            date_freq[w] = {i}

for i in date_freq:
    date_freq[i] = len(date_freq[i])

# In[25]:


total_vocab_size = len(date_freq)
total_vocab_size

# In[26]:


date_freq

# In[27]:


total_vocab = [x for x in date_freq]
total_vocab

# In[28]:


print(total_vocab[:20])


# In[29]:


def doc_freq(word):
    indice = 0
    try:
        indice = date_freq[word]
    except:
        pass
    return indice


# In[30]:


doc_id = 0

tf_idf = {}
len_docs = len(processed_text)

for i in range(len(processed_text)):

    tokens = processed_text[i]

    counter = Counter(tokens)
    words_count = len(tokens)
    unique_token = np.unique(tokens)
    for token in unique_token:
        tf = counter[token] / words_count
        doc_fre = doc_freq(token)
        idf = np.log((len_docs + 1) / (doc_fre + 1))

        tf_idf[doc_id, token] = tf * idf

    doc_id += 1

# In[31]:


tf_idf
# a bibliometric review of the waqf literature muneer m  alshater m  kabir hassan mamunur rashid  rashedul hasan jun 2022


# In[32]:


for i in tf_idf:
    print(tf_idf[i])
    tf_idf[i] *= 0.3

# In[33]:


len(tf_idf)

print("c - 166")


# In[39]:


def cal_cosine(x, y):
    cal_cosin = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
    return cal_cosin


# In[35]:


vocab_balancing = np.zeros((len(processed_text), total_vocab_size))  # fillign with zeros to rest
print("175")
for i in tf_idf:
    try:
        ind = total_vocab.index(i[1])
        vocab_balancing[i[0]][ind] = tf_idf[i]
    except:
        pass



# In[36]:

print("187")

def gen_vector(tokens):
    vocab_zeros = np.zeros((len(total_vocab)))
    print("191")

    counter = Counter(tokens)
    tok_count = len(tokens)
    print("192")
    for token in np.unique(tokens):

        tf = counter[token] / tok_count
        df = doc_freq(token)
        idf = math.log((len(processed_text) + 1) / (df + 1))
        print("198")
        try:
            ind = total_vocab.index(token)
            vocab_zeros[ind] = tf * idf
        except:
            pass
    return vocab_zeros


# In[57]:

print("211")


def search(text):
    preprocessed_text = preprocess(text)
    print("c - 219")
    print("preprocessed_text are", preprocessed_text)
    tokens_pro = word_tokenize(preprocessed_text)

    print("\nSearch input:", text)
    print("")
    print("token are", tokens_pro)

    cosine_list = []

    search_vector = gen_vector(tokens_pro)
    for d in vocab_balancing:
        # cal_cos = cal_cosine(search_vector, d)
        cal_cos = 1 - spatial.distance.cosine(search_vector, d)
        cosine_list.append(cal_cos)

    cosine_list_sort = np.array(cosine_list).argsort()[-20:][::-1]

    print("cosine list below")

    print(cosine_list_sort)
    return cosine_list_sort


# In[58]:


def search_pub(text_search):
    indices = search(text_search)
    print(indices)
    new_df = df.iloc[indices]
    results = new_df.to_dict('records')
    print(results)
    return results


# In[59]:


if __name__ == '__main__':
    print("start execution")
    crawl.craw_flow()
    search_pub("dissecting the effect of family business exposure on entrepreneurial implementation intention")
