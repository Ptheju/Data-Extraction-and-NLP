import requests
import cloudscraper
import pandas as pd
from bs4 import BeautifulSoup  
from fake_useragent import UserAgent 

article_text = []
scraper = cloudscraper.create_scraper()


df = pd.read_csv('input.csv')
for index, row in df.iterrows():
   url = row['URL']
   url_id = row['URL_ID']


   paragraphs=[]
   r = scraper.get(url)
   soup = BeautifulSoup(r.content, 'html.parser')

   
   title=soup.find('h1').text.strip()
   p=soup.find_all('p')
   for paragraph in p:
        paragraph=paragraph.text.strip()
        paragraphs.append(paragraph)
   text=''.join(paragraphs)

   #Joining the title and the content
   text=title+" "+text
   
   #Saving the text in a file
   file_name =  str(url_id) + '.txt'
   with open(file_name, 'w',encoding='utf-8') as file:
    file.write(text)

   #Appending each file
   article_text.append(file_name)

#Adding a new column which contains the text file
df = df.assign(Extracted_Text = article_text)
file_name = 'input_with_.txt.csv'
 
# saving the csv
df.to_csv(file_name)