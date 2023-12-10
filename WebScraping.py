# Use BeautifulSoup, requests and pandas libraries for web scraping the required information
# Analyze the HTML code of a webpage to find the relevant information
# Store the extracted data as a CSV file and SQL Database

# pandas library for data storage and manipulation
# BeautifulSoup library for interpreting the HTML document
# requests library to communicate with the web page
# sqlite3 for creating the database instance

# pip install pandas
# pip install bs4


import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
#the database name
db_name = 'Movies.db'
#table name for storing the record
table_name = 'Top_50'
#CSV path for saving the record
csv_path = r'C:\Users\esraa\Desktop\Python_Projects\IBM\WebScraping_Movies/top_50_films.csv'
#the entities to be saved
df = pd.DataFrame(columns=["Average Rank","Film","Year"])
# since it require only the top 50 results, we'll require a loop counter initialized to 0
count = 0


#load the entire web page as an HTML document
html_page = requests.get(url).text
#parse the text in the HTML format using BeautifulSoup to enable extraction of relevant information
data = BeautifulSoup(html_page, 'html.parser')

# Scraping of required information
tables = data.find_all('tbody')  #gets the body of all the tables in the web page
rows = tables[0].find_all('tr')  #gets all the rows of the first table


#iterate over the rows to find the required data
#Check for the loop counter to restrict to 50 entries
#Extract all the td data objects in the row and save them to col
#Check if the length of col is 0, that is, if there is no data in a current row. This is important since, many times there are merged rows that are not apparent in the web page.
#Create a dictionary data_dict with the keys same as the columns of the dataframe created for recording the output earlier and corresponding values from the first three headers of data.
#Convert the dictionary to a dataframe and concatenate it with the existing one. This way, the data keeps getting appended to the dataframe with every iteration of the loop.
#Increment the loop counter.
#Once the counter hits 50, stop iterating over rows and break the loop.
for row in rows:
    if count<50:
        col = row.find_all('td')
        if len(col)!=0:
            data_dict = {"Average Rank": col[0].contents[0],
                         "Film": col[1].contents[0],
                         "Year": col[2].contents[0]}
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1], ignore_index=True)
            count+=1
    else:
        break


print(df)



############# Storing the Data in a Database #############
# save the dataframe to a CSV file
df.to_csv(csv_path)

# To store the required data in a database, we first need to initialize a connection to the database, 
# save the dataframe as a table, and then close the connection.
conn = sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()


# This database can now be used to retrieve the relevant information using SQL queries.