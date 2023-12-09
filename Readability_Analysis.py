import pandas as pd
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



Avg_sentence_length = []
Percentage_of_Complex_words  =  []
Fog_Index = []
Complex_word_count =  []
Avg_syllable_word_count =[]
Word_Count = []

df = pd.read_csv('Output.csv')

for text in df['Extracted_Text2']:
    cleaned = []
    
    text = open(text,encoding="utf8").read()
    text = text.lower()
    tokenized_text = word_tokenize(text)

    #Average length of sentence
    sentences = len(text.split('.'))
    avg_length = len(tokenized_text) / sentences
    Avg_sentence_length.append(round(avg_length,2))


    #Percentage of Complex words 
    
    text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
    tokenized_text1 = word_tokenize(text)

    #Counting the complex words
    count = 0
    for word in tokenized_text1:
        d = {}.fromkeys('aeiou',0)
        Flag = False
        for letter in word:
            if letter in d:
                d[letter] += 1
        for q in d.values():
            if q > 2:
                Flag = True
        if Flag:
            count += 1
            
    Complex_word_count.append(count)
    Total_word_count = len(tokenized_text1)
    Percentage = count*100/Total_word_count
    Percentage_of_Complex_words.append(round(Percentage,2))

    FogIndex = 0.4*(avg_length+Percentage)
    Fog_Index.append(round(FogIndex,2))
    

    #Word Count using nltk stopwords
    stop = stopwords.words('english')
    cleaned = []
    for word in tokenized_text1:
        if word not in stop:
            cleaned.append(word)
    
    Word_Count.append(len(cleaned))

    #Function for Syllables in each word
    
    def syllable_count(word):
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        if word[0] in vowels:
            count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                count += 1
                if word.endswith("e"):
                    count -= 1
        if count == 0:
            count += 1
        return count

    sum = 0 
    for word in tokenized_text1:
        sum += syllable_count(word)
    
   
    syllable_count_per_word = (sum) / (Total_word_count)
    Avg_syllable_word_count.append(round(syllable_count_per_word,2))



df = df.assign( PERCENTAGE_OF_COMPLEX_WORDS = Percentage_of_Complex_words)
df = df.assign(FOG_INDEX = Fog_Index)
df = df.assign( AVG_NUMBER_OF_WORDS_PER_SENTENCE = Avg_sentence_length)
df = df.assign(COMPLEX_WORD_COUNT = Complex_word_count)
df = df.assign(WORD_COUNT = Word_Count)
df = df.assign(SYLLABLE_PER_WORD = Avg_syllable_word_count)

df.to_csv('Final_Output.csv')