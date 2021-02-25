import csv
from nltk.stem import PorterStemmer
import numpy as np


def tokenization(data):
    for i in range(10):
        data = data.replace(str(i), ' ')
    return data.replace('\r\n', ' ').replace(',', ' ').replace('.', ' ').replace('(', ' ') \
        .replace(')', ' ').replace('?', ' ').replace('`', ' ').replace('@', ' ').replace('%', ' ') \
        .replace('!', ' ').replace('-', ' ').replace('\'', ' ').replace('\"', ' ').replace(':', ' ') \
        .replace(';', ' ').replace('_', ' ').replace('/', ' ').replace('#', ' ').replace('*', ' ') \
        .replace('&', ' ').replace('$', ' ').replace('{', ' ').replace('}', ' ').split()


def lowercasing(data):
    return [x.lower() for x in data]


def stemming(data):
    stemmer = PorterStemmer()
    return [stemmer.stem(x) for x in data]


def remove_stopwords(data):
    with open('stopwords.txt') as sw:
        stop_words = sw.read()
        return [x for x in data if (x not in stop_words)]


def extract_vocabulary(docs):
    result_set = set()
    for doc in docs:
        token_list = tokenization(doc)
        lower_token_list = lowercasing(token_list)
        stemmed_token_list = stemming(lower_token_list)
        remove_stopword_list = remove_stopwords(stemmed_token_list)
        result_set.update(remove_stopword_list)
    return list(result_set)


def count_docs(docs):
    return len(docs)


def count_docs_in_class(docs_class, class_index):
    return len(docs_class[class_index])


def concatenate_text_of_all_docs_in_class(docs_class, class_index, V):
    result_list = []
    for doc in docs_class[class_index]:
        token_list = tokenization(doc)
        lower_token_list = lowercasing(token_list)
        stemmed_token_list = stemming(lower_token_list)
        remove_stopword_list = remove_stopwords(stemmed_token_list)
        temp_list = []
        for w in remove_stopword_list:
            if w in V:
                temp_list.append(w)

        result_list = [*result_list, *temp_list]
    return result_list


def count_tokens_of_term(text_list, term):
    cnt = 0
    for text in text_list:
        if text == term:
            cnt += 1
    return cnt


def extract_tokens_from_doc(vocabularys, doc):
    result = []
    token_list = tokenization(doc)
    lower_token_list = lowercasing(token_list)
    stemmed_token_list = stemming(lower_token_list)
    remove_stopword_list = remove_stopwords(stemmed_token_list)
    for word in remove_stopword_list:
        if word in vocabularys:
            result.append(word)
    return result


train_docs_class_list = []
test_docs_index_list = list(range(1, 1010))
train_docs_list = []
with open('trainingdata.txt') as csvfile:
    rows = csv.reader(csvfile, delimiter=' ')
    for row in rows:
        file_list = []
        for col in row[1:-1]:
            f = open('recipe_dataset/' + col + '.txt', mode='r')
            file_text = f.read()
            file_list.append(file_text)
            train_docs_list.append(file_text)
            f.close()
            test_docs_index_list.remove(int(col))
        train_docs_class_list.append(file_list)

text_all_class_list = []
for class_index in range(11):
    text_all_list = []
    for doc in train_docs_class_list[class_index]:
        token_list = tokenization(doc)
        lower_token_list = lowercasing(token_list)
        stemmed_token_list = stemming(lower_token_list)
        remove_stopword_list = remove_stopwords(stemmed_token_list)
        text_all_list.append(remove_stopword_list)
    text_all_class_list.append(text_all_list)

chi_square_list = []
V = extract_vocabulary(train_docs_list)
for class_index in range(11):
    for term in V:
        on_topic_present = 0
        off_topic_present = 0
        on_topic_absent = 0
        off_topic_absent = 0
        for docs_class_index in range(11):
            for texts in text_all_class_list[docs_class_index]:
                if (term in texts) and (docs_class_index == class_index):
                    on_topic_present += 1
                elif (term in texts) and (docs_class_index != class_index):
                    off_topic_present += 1
                elif (term not in texts) and (docs_class_index == class_index):
                    on_topic_absent += 1
                elif (term not in texts) and (docs_class_index != class_index):
                    off_topic_absent += 1
        N = on_topic_present + off_topic_present + on_topic_absent + off_topic_absent
        on_topic = on_topic_present + on_topic_absent
        off_topic = off_topic_present + off_topic_absent
        present = on_topic_present + off_topic_present
        absent = on_topic_absent + off_topic_absent
        expected_on_topic_present = N * (on_topic/N) * (present/N)
        expected_off_topic_present = N * (off_topic/N) * (present/N)
        expected_on_topic_absent = N * (on_topic/N) * (absent/N)
        expected_off_topic_absent = N * (off_topic/N) * (absent/N)

        chi_square = ((
            (on_topic_present-expected_on_topic_present)**2)/expected_on_topic_present) + ((
                (off_topic_present-expected_off_topic_present)**2)/expected_off_topic_present) + ((
                    (on_topic_absent-expected_on_topic_absent)**2)/expected_on_topic_absent) + ((
                        (off_topic_absent-expected_off_topic_absent)**2)/expected_off_topic_absent)

        chi_square_list.append(
            {'term': term, 'class_index': class_index, 'chi-square': chi_square})

term_list = sorted(
    chi_square_list, key=lambda i: i['chi-square'], reverse=True)[:500]

new_train_docs_list = []
for term in term_list:
    new_train_docs_list.append(term['term'])

V = new_train_docs_list
N = count_docs(train_docs_list)
prior = []
condprob = []
for class_index in range(11):
    Nc = count_docs_in_class(train_docs_class_list, class_index)
    prior.append(Nc / N)
    text_c = concatenate_text_of_all_docs_in_class(
        train_docs_class_list, class_index, V)

    total_number_of_terms_in_d = 0
    for t in V:
        total_number_of_terms_in_d += count_tokens_of_term(text_c, t)
    condprob_term_dict = {}
    for t in V:
        Tct = count_tokens_of_term(text_c, t)
        condprob_term = (Tct + 1) / (total_number_of_terms_in_d + len(V))
        condprob_term_dict[t] = condprob_term
    condprob.append(condprob_term_dict)


def predict_class(file_text):
    W = extract_tokens_from_doc(V, file_text)
    score_list = []
    for class_index in range(11):
        score = np.log(prior[class_index])
        for t in W:
            score += np.log(condprob[class_index][t])
        score_list.append(score)

    return score_list.index(max(score_list)) + 1


def get_three_docs(type_id):
    return train_docs_class_list[type_id][:3]
