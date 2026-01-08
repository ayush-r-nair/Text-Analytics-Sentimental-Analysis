import nltk
from nltk.corpus import cmudict
from .config import PRONOUNS, POSITIVE_WORDS_PATH, NEGATIVE_WORDS_PATH

nltk.download("cmudict", quiet=True)
d=cmudict.dict()

def load_sentiment_words(path):
    words=set()
    with open(path, encoding="latin-1") as f:
        for line in f:
            words.add(line.strip().lower())
    return words

POSITIVE_WORDS = load_sentiment_words(POSITIVE_WORDS_PATH)
NEGATIVE_WORDS = load_sentiment_words(NEGATIVE_WORDS_PATH)

def count_syllables(word):
    word=word.lower()
    if word in d:
        return len([p for p in d[word][0] if p[-1].isdigit()])
    return max(1, sum(1 for c in word if c in "aeiouy"))

def compute_metrics(words, sentences, clean_words):
    word_count=len(words)
    sentence_count=max(1, len(sentences))

    positive_score=0
    negative_score=0
    personal_pronouns=0
    complex_count=0
    total_syllables=0
    char_count=0

    for w in words:
        wl=w.lower()
        char_count+=len(w)

        if wl in POSITIVE_WORDS:
            positive_score += 1
        if wl in NEGATIVE_WORDS:
            negative_score += 1
        if wl in PRONOUNS:
            personal_pronouns += 1

        syll=count_syllables(wl)
        total_syllables+=syll
        if syll>=2:
            complex_count+=1

    cleaned_word_count=len(clean_words)

    polarity_score=(positive_score-negative_score)/((positive_score+negative_score)+1e-6)
    subjectivity_score =(positive_score+negative_score)/(cleaned_word_count+1e-6)
    avg_sentence_length=word_count/sentence_count
    pct_complex=complex_count/word_count
    fog_index=0.4*(avg_sentence_length+pct_complex)
    avg_word_length=char_count/word_count
    syllable_per_word=total_syllables/word_count

    return [
        positive_score,
        negative_score,
        polarity_score,
        subjectivity_score,
        avg_sentence_length,
        pct_complex,
        fog_index,
        avg_sentence_length,
        complex_count,
        cleaned_word_count,
        syllable_per_word,
        personal_pronouns,
        avg_word_length
    ]
