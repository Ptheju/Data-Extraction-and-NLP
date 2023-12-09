
Input.xlsx was downloaded as csv file.
URLs and URL_ID extracted from the columns of Input dataframe, were used in Data_Extraction python file to extract the title and content of our article.
.txt files were stored as the values for new assigned column 'Extracted_Text'.
Sentimental Analysis - StopWords and MasterDictionary from drive were downloaded and all the files are opened in Sentimental_Analysis python file.
Looping through .txt files from Extracted_Text column, Sentimental Analysis was carried out to compute the variables.
Readability_Analysis python file gives our Final_Output. 


Note:
I could not extract texts from 8 URLs. I used except to skip them.
Cloudscraper is also used to overcome possible blockages to automated requests.
