#Libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict
import os

#Donwload these only once
nltk.download('punkt', quiet=True)
nltk.download('cmudict', quiet=True)

d = cmudict.dict()

#Custom syllable counter using NLTK
def count_syllable(word):
    word=word.lower()
    if word not in d :
        return 0
    return len([ph for ph in d[word][0] if ph[-1].isdigit()])

#StopWord List
file_paths = [
    r"StopWords\StopWords\StopWords_Auditor.txt",
    r"StopWords\StopWords\StopWords_Currencies.txt",
    r"StopWords\StopWords\StopWords_DatesandNumbers.txt",
    r"StopWords\StopWords\StopWords_Generic.txt",
    r"StopWords\StopWords\StopWords_GenericLong.txt",
    r"StopWords\StopWords\StopWords_Geographic.txt",
    r"StopWords\StopWords\StopWords_Names.txt"
]

stopwords_set=set()

for path in file_paths:
    with open(path,'r',encoding='latin-1') as f:
        for line in f :
            words=line.split('|')[0].strip()
            for word in words.split() :
                stopwords_set.add(word)

stopwords=list(stopwords_set)

#Positive Word and Negative Word list
paths=[
    r"MasterDictionary\MasterDictionary\negative-words.txt",
    r"MasterDictionary\MasterDictionary\positive-words.txt"
]

positive_set=set()
negative_set=set()

with open(paths[0],'r',encoding='latin-1') as f :
    for word in f :
        negative_set.add(word[:-1])
        
with open(paths[1],'r') as f :
    for word in f :
        positive_set.add(word[:-1])

negativewords=list(negative_set)  
positivewords=list(positive_set)

#Pronouns list
pronouns=["i", "we", "my", "ours","us"]


#Article Extraction
def extract_article(url_id,url):
    
    page=requests.get(url)

    soup=BeautifulSoup(page.text, 'html.parser')
    
    articles = soup.find_all('article')
    content = ""
    
    for article in articles:
        for tag in article.descendants:
            if tag.name in ['h1', 'h2', 'h3', 'p']:
                text = tag.get_text(strip=True)
                if text:
                    content += text + "\n"
                    
    with open(f"Extracted Articles/{url_id}.txt",'w') as f:
        f.write(content)
    return content

#Text Analysis
def text_analysis():
    df=pd.read_excel("Input.xlsx")
    rows=df.values
    result=[]
    
    for i,j in rows :
        
        url_id=i
        url=j
        
        #Variable initilization
        article=extract_article(url_id,url)
        
        words=word_tokenize(article)
        
        sentences=sent_tokenize(article)
        
        word_count=len(words)
        
        sentence_count=len(sentences)
        
        total_syllables=0
        
        clean_words=[]
        
        p=0
        n=0
        
        personal_pronouns=0
        
        complex_count=0
        
        char_count=0
        
        for word in words :
            char_count+=len(word)
            
            if word not in stopwords and word not in "!?,.":
                clean_words.append(word)
                
            if word in positivewords :
                p+=1
                
            if word in negativewords :
                n+=1
                
            if word.lower() in pronouns :
                personal_pronouns+=1
                
            syllable_count_per_word=count_syllable(word)
            total_syllables+=syllable_count_per_word
            
            if(syllable_count_per_word>=2):
                complex_count+=1
                
            cleaned_word_count=len(clean_words)
            
        #All the attributes found
        positive_score=p
        negative_score=n
        polarity_score=(p-n)/((p+n)+0.000001)
        subjectivity_score=(p+n)/((cleaned_word_count)+0.000001)
        average_sentence_length=word_count/sentence_count
        percentage_of_complex_words=complex_count/word_count
        fog_index=0.4*(average_sentence_length+percentage_of_complex_words)
        average_no_of_words_per_sentence=word_count/sentence_count
        complex_word_count=complex_count
        total_cleaned_words=cleaned_word_count
        syllable_per_word=total_syllables/word_count
        personal_pronouns_count=personal_pronouns
        average_word_length=char_count/word_count
        
        #Stroing the values in list
        columns_values=[positive_score,negative_score,polarity_score,subjectivity_score,average_sentence_length,
                        percentage_of_complex_words,fog_index,average_no_of_words_per_sentence,complex_word_count,
                        total_cleaned_words,syllable_per_word,personal_pronouns_count,average_word_length]
        
        result.append(columns_values)
        
    return result

def fill_output():
    value_list=text_analysis()
    df=pd.read_excel("Output Data Structure.xlsx")
    df.iloc[:,2:]=value_list
    df.to_excel("Output Data Structure.xlsx", index=False)

if __name__ == "__main__":
    fill_output()