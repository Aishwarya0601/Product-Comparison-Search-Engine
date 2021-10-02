# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 12:07:31 2021

@author: AISHWARYA
"""
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import csv

df = pd.read_csv("C:/Users/AISHWARYA/Downloads/ProductsDataFinal.csv")
#Choosing only required columns
df_new = df.iloc[:,[0,1,3,5,6]]
df_new.to_csv('ProductsData_CSV1.csv', header=True, index=None)

#Converting csv to text file for text analysis
csv_file = "ProductsData_CSV1.csv"
txt_file = "ProductsData_TXT1.txt"
with open(txt_file, "w",encoding="utf-8") as my_output_file:
    with open(csv_file, "r",encoding="utf-8" ) as my_input_file:
        [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()

#Function to remove special characters and punctuations
def remove_punctuations(text):
  text=text.lower()
  punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
  for i in text:
    if i in punc:
      text=text.replace(i,"")
  return text

#Reading the file to know the number of documents
documents=[]
with open("ProductsData_TXT1.txt","r",encoding='utf-8') as infile:
  for line in infile:
      documents.append(line)
print("Document length : ",len(documents)) 

#Performing tokenisation of each document
for i in range(len(documents)):
  documents[i] = remove_punctuations(documents[i])
  text_tokens = word_tokenize(documents[i])
  documents[i] = [word for word in text_tokens if not word in stopwords.words()]
print(documents[0])
total_tokens=[]
for i in range(len(documents)):
  for j in documents[i]:
    if j not in total_tokens:
        if(j.isnumeric()==False):
          total_tokens.append(j)
print("Total number of tokens : ",len(total_tokens))

#Calculating frequency of each token in each document
termPostingLists={}
for i in total_tokens:
  temp=[]
  for j in range(len(documents)):
    if i in documents[j]:
      temp.append(j+1)
  termPostingLists[i]=temp

#Storing the term posting list in the file  
f = open("IndexedDocuments1.txt","w",encoding='utf-8')
for l in termPostingLists:
    termPostingLists[l] = map(str,termPostingLists[l])
    listString = ",".join(termPostingLists[l])
    string = l + " : " + listString + "\n"
    f.write(string)
f.close()



"""try:
    geeky_file = open('geekyfile.txt', 'wt')
    geeky_file.write(str(printing))
    geeky_file.close()
  
except:
    print("Unable to write to file")
print("The first 10 dictionary terms and their posing lists are")
for i in printing:
  print(i,":",printing[i],end="\n\n")

driver = webdriver.Chrome(ChromeDriverManager().install())
url = "https://www.simplinamdharis.com/categories/home-grocery-attamaidaflours/cid-CI68408935.aspx"
driver.get(url)
time.sleep(3) #if you want to wait 3 seconds for the page to load
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')"""





