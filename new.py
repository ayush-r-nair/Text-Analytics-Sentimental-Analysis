# main.py

import os
import requests
import pandas as pd
import nltk
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict

# Download required NLTK resources (only if not already present)
nltk.download('punkt', quiet=True)
nltk.download('cmudict', quiet=True)
d = cmudict.dict()

# --------- Configuration ---------
STOPWORDS_DIR = os.path.join("StopWords", "StopWords")
DICT_DIR = os.path.join("MasterDictionary", "MasterDictionary")
EXTRACTED_DIR = "Extracted Articles"
INPUT_FILE = "Input.xlsx"
OUTPUT_FILE = "Output Data Structure.xlsx"

# --------- Utility Functions ---------
def count_syllable(word):
    """Count syllables in a word using CMU Pronouncing Dictionary."""
    word = word.lower()
    if word not in d:
        return 0
    return len([ph for ph in d[word][0] if ph[-1].isdigit()])

def load_stopwords():
    """Load custom stopwords from provided files."""
    file_names = [
        "StopWords_Auditor.txt",
        "StopWords_Currencies.txt",
        "StopWords_DatesandNumbers.txt",
        "StopWords_Generic.txt",
        "StopWords_GenericLong.txt",
        "StopWords_Geographic.txt",
        "StopWords_Names.txt",
    ]
    stopwords_set = set()
    for fname in file_names:
        path = os.path.join(STOPWORDS_DIR, fname)
        try:
            with open(path, 'r', encoding='latin-1') as f:
                for line in f:
                    words = line.split('|')[0].strip()
                    for word in words.split():
                        stopwords_set.add(word)
        except FileNotFoundError:
            print(f"Warning: Stopword file not found: {path}")
    return list(stopwords_set)

def load_sentiment_words():
    """Load positive and negative word lists."""
    negative_path = os.path.join(DICT_DIR, "negative-words.txt")
    positive_path = os.path.join(DICT_DIR, "positive-words.txt")
    negative_set, positive_set = set(), set()
    try:
        with open(negative_path, 'r', encoding='latin-1') as f:
            for word in f:
                word = word.strip()
                if word and not word.startswith(";"):
                    negative_set.add(word)
    except FileNotFoundError:
        print(f"Warning: Negative words file not found: {negative_path}")
    try:
        with open(positive_path, 'r', encoding='latin-1') as f:
            for word in f:
                word = word.strip()
                if word and not word.startswith(";"):
                    positive_set.add(word)
    except FileNotFoundError:
        print(f"Warning: Positive words file not found: {positive_path}")
    return list(positive_set), list(negative_set)

def ensure_dir(directory):
    """Ensure a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# --------- Main Processing Functions ---------
def extract_article(url_id, url):
    """Extract article text from a URL and save to a text file."""
    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return ""
    soup = BeautifulSoup(page.text, 'html.parser')
    articles = soup.find_all('article')
    content = ""
    for article in articles:
        for tag in article.descendants:
            if tag.name in ['h1', 'h2', 'h3', 'p']:
                text = tag.get_text(strip=True)
                if text:
                    content += text + "\n"
    ensure_dir(EXTRACTED_DIR)
    with open(os.path.join(EXTRACTED_DIR, f"{url_id}.txt"), 'w', encoding='utf-8') as f:
        f.write(content)
    return content

def text_analysis():
    """Perform text analysis on articles listed in the input Excel file."""
    try:
        df = pd.read_excel(INPUT_FILE)
    except Exception as e:
        print(f"Error reading input file: {e}")
        return []
    rows = df.values
    stopwords = load_stopwords()
    positivewords, negativewords = load_sentiment_words()
    pronouns = {"i", "we", "my", "ours", "us"}
    results = []
    for url_id, url in rows:
        print(f"Processing: {url_id} - {url}")
        article = extract_article(url_id, url)
        if not article:
            results.append([None]*13)
            continue
        words = word_tokenize(article)
        sentences = sent_tokenize(article)
        word_count = len(words)
        sentence_count = len(sentences) if sentences else 1
        total_syllables = 0
        clean_words = []
        p, n = 0, 0
        personal_pronouns = 0
        complex_count = 0
        char_count = 0
        for word in words:
            char_count += len(word)
            if word.lower() not in stopwords and word not in "!?,.":
                clean_words.append(word)
            if word.lower() in positivewords:
                p += 1
            if word.lower() in negativewords:
                n += 1
            if word.lower() in pronouns:
                personal_pronouns += 1
            syllable_count_per_word = count_syllable(word)
            total_syllables += syllable_count_per_word
            if syllable_count_per_word >= 2:
                complex_count += 1
        cleaned_word_count = len(clean_words)
        positive_score = p
        negative_score = n
        polarity_score = (p - n) / ((p + n) + 1e-6)
        subjectivity_score = (p + n) / (cleaned_word_count + 1e-6)
        average_sentence_length = word_count / sentence_count
        percentage_of_complex_words = complex_count / word_count if word_count else 0
        fog_index = 0.4 * (average_sentence_length + percentage_of_complex_words)
        average_no_of_words_per_sentence = word_count / sentence_count
        complex_word_count = complex_count
        total_cleaned_words = cleaned_word_count
        syllable_per_word = total_syllables / word_count if word_count else 0
        personal_pronouns_count = personal_pronouns
        average_word_length = char_count / word_count if word_count else 0
        columns_values = [
            positive_score, negative_score, polarity_score, subjectivity_score, average_sentence_length,
            percentage_of_complex_words, fog_index, average_no_of_words_per_sentence, complex_word_count,
            total_cleaned_words, syllable_per_word, personal_pronouns_count, average_word_length
        ]
        results.append(columns_values)
    return results

def fill_output():
    """Fill the output Excel file with analysis results."""
    value_list = text_analysis()
    try:
        df = pd.read_excel(OUTPUT_FILE)
        df.iloc[:, 2:] = value_list
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"Results saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    fill_output()