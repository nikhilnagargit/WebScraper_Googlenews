"""@author - Nikhil Nagar
"""


# Assignment submission by -  "Nikhil Nagar"  for internship opportunity in "Chattel Technologies"

# Overview : 1. This webscraper collects the news data and save it to csv files.(to save your time..it is limited to saving of 10 news article)
#            2. Also a function is implemented to search a keyword in news and return sentences conatining the keyword. 

#libraries to install -   
# pip install nltk
# pip install requests
# pip install lxml
# pip install bs4
# pip install newspaper3k


import requests
from bs4 import BeautifulSoup
from newspaper import Article
import pandas
from nltk.tokenize import word_tokenize,sent_tokenize
import time

#fetching base soup page
print("starting execution...please wait")

url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen"
res = requests.get(url)
soup = BeautifulSoup(res.content ,"html.parser")

#fetching top 10 basic containers of news articles
list_of_newsblocks = soup.find_all('div',{"class":"xrnccd F6Welf R7GTQ keNKEd j7vNaf"},limit=10)


#function to preprocess data from article link and form a data_row
def create_datarow(link):
    article = Article(link,language="en")
    
    article.download()
    article.parse()
    article.nlp()
    row ={}
    row["Title"]=article.title
    row["Summary"]=(article.summary).replace('\n','')
    row["Raw_news"]=(article.text).replace('\n','')
    row["Date"]=article.publish_date
    row['Link']=link
    print("\n\n")
    for key in row.keys():
        print(key,":",row[key])
        print()
    return row


print("\n\n\nCSV file will be saved after complition of processing.\n\nYou can search words in raw news after saving 10 articles in csv file.\n\n")
time.sleep(3)

# two data lists for tables - 1. main_news_table  2. sub_news_table
main_news_rows_list = []
sub_news_rows_list =[]
#looping through each news_block and collecting main_news and sub_news
for newsblock in list_of_newsblocks:
    
    main_news_link ="https://news.google.com" + newsblock.find('h3',{"class":"ipQwMb ekueJc gEATFF RD0gLb"}).a["href"][1:]
    sub_news_link ="https://news.google.com" + newsblock.find('h4',{"class":"ipQwMb ekueJc gEATFF RD0gLb"}).a["href"][1:]
    #filling the data rows of main_news_table
    main_news_rows_list.append(create_datarow(main_news_link))
    #filling the data rows of sub_news_table
    sub_news_rows_list.append(create_datarow(sub_news_link))
    
    
    
    
#creating dataframe with pandas for both tables
main_news_dataframe = pandas.DataFrame(main_news_rows_list)
main_news_dataframe.to_csv('Main_news_table.csv') 
sub_news_dataframe = pandas.DataFrame(sub_news_rows_list)
sub_news_dataframe.to_csv('Sub_news_table.csv') 

print("\n\nProcess Compelete. check csv files.")





#part-2   search function to find words in headlines of news

def search_word_in_raw_news(word):
    global main_news_dataframe
    global sub_news_dataframe
    #putting together all text in which, word need to be searched
    text = ''
    for i in main_news_dataframe.Raw_news:
        text=text+i
    for i in sub_news_dataframe.Raw_news:
        text=text+i
        
    search_result=[]
    
    list_of_sentences = sent_tokenize(text)
    for sentence in list_of_sentences:
        if(word in word_tokenize(sentence)):
            search_result.append(sentence)
    if(search_result==[]):
        print("No Search Result Found in Raw News Text.")
    else:
        print("Search Result : \n")
        print(search_result)
    
    
word = input("Enter a word to search in Raw News. >>> ")
search_word_in_raw_news(word)
    




    


#this code is implemented by "Nikhil Nagar"


   



