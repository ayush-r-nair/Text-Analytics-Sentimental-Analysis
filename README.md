# Text Analytics and Sentiment Analysis

A Python-based project that extracts, cleans, and analyzes web article content using Natural Language Processing (NLP) techniques. It calculates both linguistic and sentiment-based metrics such as readability (Fog Index), polarity, subjectivity, and more.

---

## 🚀 Features

- 🔍 Scrapes articles from URLs listed in an Excel file
- ✨ Cleans and tokenizes article text using NLTK
- 📈 Calculates:
  - Positive & Negative Scores
  - Polarity & Subjectivity
  - Average Sentence Length
  - Fog Index (Readability)
  - Syllables per Word
  - Complex Word Count
  - Personal Pronoun Count
- 📊 Outputs analysis results into an Excel file
- 🧠 Uses custom dictionaries for stopwords and sentiment words

---

## 🗂️ Project Structure

```
Text-Analytics-Sentiment-Analysis/
├── main.py
├── requirements.txt
├── Input.xlsx
├── Output Data Structure.xlsx
├── README.md
├── .gitignore
├── StopWords/
│   └── StopWords_*.txt
├── MasterDictionary/
│   ├── positive-words.txt
│   └── negative-words.txt
├── Extracted Articles/
│   └── [Article_Text_Files]
```

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ayush-r-nair/Text-Analytics-Sentimental-Analysis.git
cd Text-Analytics-Sentimental-Analysis
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ How to Use

1. Add URLs to `Input.xlsx` in the format:
   ```
   | URL_ID | URL |
   ```

2. Make sure the following folders are present and populated:
   - `StopWords/` with custom stopword `.txt` files
   - `MasterDictionary/` with `positive-words.txt` and `negative-words.txt`

3. Run the script:

```bash
python main.py
```

4. The extracted text is saved to `Extracted Articles/`, and results are written to `Output Data Structure.xlsx`.

---

## 📊 Output Metrics Explained

| Metric                       | Description |
|------------------------------|-------------|
| Positive Score               | Count of positive words |
| Negative Score               | Count of negative words |
| Polarity Score               | (Positive - Negative) / (Positive + Negative + ε) |
| Subjectivity Score           | (Positive + Negative) / Total Cleaned Words |
| Average Sentence Length      | Words per sentence |
| Complex Word Count           | Words with ≥ 2 syllables |
| Percentage of Complex Words  | Complex / Total Words |
| Fog Index                    | 0.4 × (ASL + % Complex Words) |
| Syllables per Word           | Average syllables per word |
| Personal Pronoun Count       | Count of “I”, “we”, “my”, “us”, “ours” |
| Average Word Length          | Total characters / Total words |

---

## 📚 Technologies Used

- **Python**
- **NLTK** – for tokenization and syllable counting
- **BeautifulSoup** – for web scraping
- **Pandas** – for reading/writing Excel
- **Requests** – for fetching URLs

---
