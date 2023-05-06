#importing libraries
import requests
from bs4 import BeautifulSoup as bs
import re
import time


#Setting the URL to Medium's homepage
url = "https://medium.com/"


#Sending a GET request to the URL and parsing the HTML response using Beautiful Soup
res = requests.get(url)
soup = bs(res.text, "html.parser")

#print(res.text)

#Finding the section with class "pw-homefeed", which contains the articles
news_article = soup.find("section", {"class": "pw-homefeed"})

print(news_article)

#Finding all the 'a' elements with 'href' attributes containing an https URL, and storing them in a set to remove duplicates
articles = set(map(lambda x: x.get('href'), news_article.find_all("a", attrs={'href': re.compile("^https://")})))

#len(articles)
#print(articles)

#Iterating through the set of articles

for article in articles:
    url = article
    print(url)
    
    # Send a GET request to the article URL and parse the HTML response
    res = requests.get(article)
    soup = bs(res.text, "html.parser")
    
    # Extract the title, description paragraphs, and author of the article
    title = (soup.find("h1", {"class": "pw-post-title"}).text if soup.find("h1", {"class": "pw-post-title"}) else '')
    descs = list(map(lambda x: x.text, soup.find_all("p", {"class": "pw-post-body-paragraph"})))
    author = (soup.find("div", {"class": "pw-author"}).text if soup.find("div", {"class": "pw-author"}) else '')
    
    # Print the extracted information if it's available
    if author and title and descs:
        print(f"Author: {author}\nTitle: {title}\nDesc len: {len(descs)}\n")
    time.sleep(5)
