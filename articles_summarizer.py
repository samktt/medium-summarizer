# Importing libraries
import requests
from bs4 import BeautifulSoup as bs
from transformers import pipeline
import re
import time

# Initialize the text summarization pipeline with the BART model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Set the URL to Medium's homepage
url = "https://medium.com/"

# Send a GET request to the URL
res = requests.get(url)

# Parse the HTML response using Beautiful Soup
soup = bs(res.text, "html.parser")

# Find the section with class "pw-homefeed", which contains the articles
news_article = soup.find("section", {"class": "pw-homefeed"})

# Find all the 'a' elements with 'href' attributes containing an https URL
a_elements = news_article.find_all("a", attrs={'href': re.compile("^https://")})

# Extract the URLs (href attributes) from the 'a' elements using a lambda function
article_urls = map(lambda x: x.get('href'), a_elements)

# Convert the list of URLs to a set to remove duplicates
unique_articles = set(article_urls)


# Function to fetch and parse article data from a given URL
def get_article_data(article_url):
    # Send a GET request to the article URL
    response = requests.get(article_url)
    # Parse the HTML response using Beautiful Soup
    soup = bs(response.text, "html.parser")

    # Find the title, description paragraphs, and author elements in the parsed HTML
    title = soup.find("h1", {"class": "pw-post-title"})
    descs = soup.find_all("p", {"class": "pw-post-body-paragraph"})
    author = soup.find("div", {"class": "pw-author"})

    # Extract text from the elements found, handling cases when elements are not found
    title_text = title.text if title else ''
    descs_text = [desc.text for desc in descs]
    author_text = author.text if author else ''

    # Combine the descriptions into a single string
    full_text = ' '.join(descs_text)


 # Truncate the input text if it's too long
    max_input_length = 512
    input_length = len(full_text.split())
    if input_length > max_input_length:
        full_text = ' '.join(full_text.split()[:max_input_length])

    # Perform text summarization using the BART model
    summary = summarizer(full_text, max_length=100, min_length=30, do_sample=False)


    # Return the extracted data in a dictionary
    return {
        'url': article_url,
        'title': title_text,
        'descs': descs_text,
        'author': author_text,
        'summary': summary[0]['summary_text']
    }



    # Iterate through the set of unique article URLs
for article in unique_articles:
    try:
        # Fetch and parse the article data
        article_data = get_article_data(article)

        # Check if the required data (author, title, descriptions) is available
        if article_data['title'] and article_data['descs']:
            # Print the extracted information in a formatted manner
            print(f"URL: {article_data['url']}")
            print(f"Author: {article_data['author']}")
            print(f"Title: {article_data['title']}")
            print(f"Summary: {article_data['summary']}\n")

        # Add a delay between requests to avoid overloading the server
        time.sleep(2)

    # Handle any exceptions that may occur during the processing of an article
    except Exception as e:
        print(f"Error while processing article {article}: {e}")
