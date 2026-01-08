import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from .config import STOPWORD_PATHS

nltk.download("punkt", quiet=True)

def load_stopwords():
    stopwords=set()
    for path in STOPWORD_PATHS:
        with open(path,encoding="latin-1") as f:
            for line in f:
                word=line.split("|")[0].strip().lower()
                if word:
                    stopwords.add(word)
    return stopwords

STOPWORDS=load_stopwords()

def tokenize_text(text):
    words=word_tokenize(text)
    sentences=sent_tokenize(text)
    return words,sentences

def clean_words(words):
    cleaned=[]
    for w in words:
        wl=w.lower()
        if wl.isalpha() and wl not in STOPWORDS:
            cleaned.append(wl)
    return cleaned
