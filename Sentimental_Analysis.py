import pandas as pd
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



#Load all the stop_words from text files of StopWords Folder

All_stop_words = []
for text_file in os.listdir('C:\\Users\\user\\Downloads\\Stop_words'):
  with open(os.path.join('C:\\Users\\user\\Downloads\\Stop_words', text_file),'r') as f:
    text = f.read()

    stop_words = word_tokenize(text)

    for word in stop_words:
       All_stop_words.append(word)

#Load Positive and Negative words from MasterDictionary

positive_words = open("C:\\Users\\user\\Downloads\\positive-words.txt").read()
positive_words = word_tokenize(positive_words)
negative_words = open("C:\\Users\\user\\Downloads\\negative-words.txt").read()
negative_words = word_tokenize(negative_words)




df = pd.read_csv('Input.csv')

Positive_Score = []
Negative_Score = []
Polarity_Score = []
Subjectivity_Score = []
Personal_pronouns = []
AVG_word_length = []

for text in df['Extracted_Text']:
    cleaned = []
    try:
      text = open(text,encoding="utf8").read()
      text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
      text = text.lower()
      tokenized_text = word_tokenize(text)

      #Cleaning the text
      for token in tokenized_text:
         if token not in All_stop_words:
            cleaned.append(token)
      
      #Positive Score
      p_score = 0
      for word in cleaned:
         if word in positive_words:
            p_score +=1
      Positive_Score.append(p_score)
      
      #Negative Score
      n_score = 0
      for word in cleaned:
         if word in negative_words:
            n_score +=1
      Negative_Score.append(n_score)

      #Polarity Score
      Polarity = (p_score-(n_score))/((p_score+(n_score))+ 0.000001)
      Polarity_Score.append(Polarity)

      #Subjectivity Score
      Subjectivity = (p_score+(n_score))/(len(cleaned)+0.000001)  
      Subjectivity_Score.append(Subjectivity)

      print(len(cleaned))
      print(p_score,n_score,Polarity,Subjectivity)

      #Personal Pronouns
      personal_pronouns_re = r'\b(I|my|we|us|ours)\b'
      count = 0
      for pronoun in personal_pronouns_re:
         count += len(re.findall(personal_pronouns_re, text)) 
    
      Personal_pronouns.append(count)

      #AVG word length
      char_count = 0
      for word in tokenized_text:
         char_count += len(word.split())
    
      Avg_word_length = char_count / len(tokenized_text)
      AVG_word_length.append(round(Avg_word_length,2))
      
    except FileNotFoundError:
         print('File not found!!', text)
         continue
    
print(len(Polarity_Score))
df = df.assign(POSITIVE_SCORE = Positive_Score)
df = df.assign(NEGATIVE_SCORE = Negative_Score)
df = df.assign(POLARITY_SCORE = Polarity_Score)
df = df.assign(SUBJECTIVITY_SCORE = Subjectivity_Score)
df = df.assign(PERSONAL_PRONOUNS = Personal_pronouns)
df = df.assign(AVG_WORD_LENGTH = AVG_word_length)

df.to_csv('Output.csv')
  
  






   