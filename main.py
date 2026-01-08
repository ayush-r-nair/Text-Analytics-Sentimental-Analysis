import pandas as pd
from src.extractor import extract_article
from src.cleaner import tokenize_text, clean_words
from src.metrics import compute_metrics

def run():
    input_df=pd.read_excel("Input.xlsx")
    results=[]

    for url_id,url in input_df.values:
        article=extract_article(url)
        if not article:
            results.append([0]*13)
            continue

        words, sentences=tokenize_text(article)
        cleaned=clean_words(words)

        metrics=compute_metrics(words, sentences, cleaned)
        results.append(metrics)
        print(url_id)

    output_df=pd.read_excel("Output Data Structure.xlsx")
    output_df.iloc[:,2:]=results
    output_df.to_excel("Output Data Structure.xlsx", index=False)

if __name__ == "__main__":
    run()
