import pandas as pd
import numpy as np
from collections import Counter

import math

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize

df = pd.read_csv("/Users/admin/PycharmProjects/cw_ir/pub.csv", index_col=False)


def convert_lower_case(data):
    return np.char.lower(data)


def remove_stop_words(data):
    stop_words = stopwords.words('english')
    words = word_tokenize(str(data))
    new_text = ""
    for w in words:
        if w not in stop_words and len(w) > 1:
            new_text = new_text + " " + w
    return new_text


def remove_punctuation(data):
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in range(len(symbols)):
        data = np.char.replace(data, symbols[i], ' ')
        data = np.char.replace(data, "  ", " ")
    data = np.char.replace(data, ',', '')
    return data


def remove_apostrophe(data):
    return np.char.replace(data, "'", "")


def stemming(data):
    stemmer = PorterStemmer()

    tokens = word_tokenize(str(data))
    new_text = ""
    for w in tokens:
        new_text = new_text + " " + stemmer.stem(w)
    return new_text


def preprocess(data):
    data = convert_lower_case(data)
    data = remove_punctuation(data)
    data = remove_apostrophe(data)
    data = remove_stop_words(data)
    data = stemming(data)
    return data


def fetch_preprocess_text(df):
    processed_text = []
    for index, item in df.iterrows():
        text = item["pub_title"] + " " + item["auth_name_extract"] + " " + item["pub_date"]
        processed_text.append(word_tokenize(str(preprocess(text))))
    return processed_text


def gen_data_freq(processed_text):
    data_freq = {}
    for i in range(len(processed_text)):
        tokens = processed_text[i]
        for w in tokens:
            try:
                data_freq[w].add(i)
            except:
                data_freq[w] = {i}
    for i in data_freq:
        data_freq[i] = len(data_freq[i])
    return data_freq


def get_total_vocab(data_frq):
    total_vocab = [x for x in data_frq]
    return total_vocab


def doc_freq(word, data_frq):
    ind = 0
    try:
        ind = data_frq[word]
    except:
        pass
    return ind


def tf_idf_conv(processed_text, data_freq_text):
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
            doc_fre = doc_freq(token, data_freq_text)
            idf = np.log((len_docs + 1) / (doc_fre + 1))
            tf_idf[doc_id, token] = tf * idf

        doc_id += 1

    for i in tf_idf:
        print(tf_idf[i])
        tf_idf[i] *= 0.3
    return tf_idf


def cosine_sim(a, b):
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return cos_sim


def fetch_gen_np(processed_text, tf_idf):

    doc_gen_np = np.zeros((len(processed_text), total_vocab_size))
    for i in tf_idf:
        try:
            ind = total_vocab.index(i[1])
            doc_gen_np[i[0]][ind] = tf_idf[i]
        except:
            pass
    return doc_gen_np


def convert_to_vector(processed_text, data_freq):
    Q = np.zeros((len(total_vocab)))

    for i in range(len(processed_text)):
        tokens = processed_text[i]
        counter = Counter(tokens)
        words_count = len(tokens)

        for token in np.unique(tokens):

            tf = counter[token] / words_count
            df = doc_freq(token, data_freq)
            idf = math.log((len(processed_text) + 1) / (df + 1))

            try:
                ind = total_vocab.index(token)
                Q[ind] = tf * idf
            except:
                pass
    return Q


#main-flow
text = fetch_preprocess_text(df)
data_freq = gen_data_freq(text)
total_vocab = get_total_vocab(data_freq)
total_vocab_size = len(data_freq)
print(total_vocab)
print(total_vocab_size)

tf_idf_all_doc = tf_idf_conv(text, data_freq)
tf_idf_vocab = fetch_gen_np(text, tf_idf_all_doc)


def search(search_input):
    preprocessed_search = preprocess(search_input)
    search_tokens = word_tokenize(preprocessed_search)
    cosines_list = []

    search_vector = convert_to_vector(search_tokens, data_freq)
    for d in tf_idf_vocab:
        result = cosine_sim(search_vector, d)
        cosines_list.append(result)

    sorted_list_indices = np.array(cosines_list).argsort()[::-1]
    new_df = df.iloc[sorted_list_indices]
    print(new_df.to_dict('records'))
    return new_df.to_dict('records')


if __name__ == '__main__':
    print("start execution")
    search("corporate stock")
