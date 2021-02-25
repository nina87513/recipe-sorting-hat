from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import numpy as np

stopwords = nltk.corpus.stopwords.words("english")
stemmer = PorterStemmer()
dot = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
num = '1234567890'

doc_all = []
for i in range(1010):
    opentxt = open("recipe_dataset/{}.txt".format(i+1), encoding="utf-8")
    t = opentxt.read().replace("\n", " ").lower()
    for a in range(len(t)):
        try:
            if t[a] in dot:
                t = t.replace(t[a], "")
        except:
            break
    doc_all.append(t)


def listn(abc):
    listn = []
    terms = abc.split()
    # terms = doctest[d-1].split()
    for each in terms:
        if each not in stopwords:
            if each[0] not in num:
                if each[0:4] not in "http":
                    listn.append(stemmer.stem(each))
    return listn


def vcount(string):
    x = {}
    for i in string:
        if i not in x:
            x[i] = 1
        else:
            x[i] += 1
    return x


def cosine(Docx, Docy, dict, doctest, tf):
    ox = []
    oy = []
    xy = []
    xword = tf[Docx-1].keys()
    yword = tf[Docy-1].keys()

    for i in xword:
        idf_wx = np.log((len(doctest))/(dict[i]))
        ox.append(tf[Docx-1][i]*idf_wx)
    for i in yword:
        idf_wy = np.log((len(doctest))/(dict[i]))
        oy.append(tf[Docy-1][i]*idf_wy)

    normx = np.sqrt(sum(np.array(ox)**2))
    normy = np.sqrt(sum(np.array(oy)**2))

    for i in xword:
        if i in yword:
            idf = np.log((len(doctest))/(dict[i]))
            x = tf[Docx-1][i]*idf/normx
            y = tf[Docy-1][i]*idf/normy
            xy.append(x*y)

    return sum(np.array(xy))


def reference(search):
    tf = []
    doctest = []
    dict = {}

    for i in range(len(stopwords)):
        for s in range(len(stopwords[i])):
            try:
                if stopwords[i][s] in dot:
                    stopwords[i] = stopwords[i].replace(stopwords[i][s], "")
            except:
                continue

    search = search.lower()
    for a in range(len(search)):
        try:
            if search[a] in dot:
                search = search.replace(search[a], "")
        except:
            break

    doctest[:] = doc_all
    doctest.append(search)

    trlist = []
    for i in range(len(doctest)):
        templi = []
        terms = doctest[i].split()
        for each in terms:
            if each not in stopwords:
                if each[0] not in num:
                    if each not in templi:
                        templi.append(each)
        for one in templi:
            trlist.append(stemmer.stem(one))

    temp = vcount(trlist)

    for i in sorted(list(temp.keys())):
        dict[i] = temp[i]

    for i in range(1, len(doctest)+1):
        tf.append(vcount(listn(doctest[i-1])))

    maxcos = []
    for i in range(1, len(doctest)):
        maxcos.append(cosine(i, 1011, dict, doctest, tf))

    commend = []
    for x in sorted(maxcos, reverse=True)[0:5]:
        commend.append(maxcos.index(x)+1)

    crit_ = open("文件編號解釋.txt")
    crit_con = crit_.read()
    crit_con = crit_con.split("\n")
    crit_con[0].split(" ")

    CC = {}
    for c in range(len(crit_con)):
        a = crit_con[c].split(" ")
        CC[a[0]] = []
        for x in range(1, (len(a))):
            CC[a[0]].extend(
                list(range(int(a[x].split("-")[0]), int(a[x].split("-")[1])+1)))

    sel = []
    for i in CC.keys():
        for n in CC[i]:
            if n in commend and i not in sel:
                print(n)
                f = open("recipe_dataset/{}.txt".format(n), encoding="utf-8")
                title = f.readline()
                content = f.read()
                sel.append(
                    {'result_type': i, 'result_title': title, 'result_text': content})
                f.close()

    return sel


if __name__ == "__main__":
    newopen = open("tomato.txt", encoding="utf-8")
    newt = newopen.read().replace("\n", " ")
    print(newt)
    ref = reference(newt)
    print(ref)
