# Medium Articles Summarizer

This Python script, articles_summarizer.py, in the medium-api project, fetches and summarizes Medium articles using the BART model. The summarized information includes the article URL, author, title, and summary.

### Dependencies
The script uses the following libraries:

requests - for sending HTTP requests
bs4 (BeautifulSoup) - for parsing HTML content
transformers - for utilizing the BART model to summarize text
re - for regular expression operations
time - for adding delays between requests

### How it works
The script initializes the text summarization pipeline with the BART model.
A GET request is sent to Medium's homepage, and the HTML response is parsed with BeautifulSoup.
The script finds the section containing the articles and extracts the unique article URLs.
For each unique article URL, the script fetches and parses the article data, including the title, description paragraphs, and author information.
The descriptions are combined into a single string and summarized using the BART model.
The extracted and summarized information is printed in a formatted manner.

### Usage
Simply run the script using Python, and it will fetch and summarize articles from the Medium homepage:
```bash
python articles_summarizer.py
```
The output will display the article URL, author, title, and summary for each article. Note that there's a delay of 2 seconds between processing each article to avoid overloading the server.

### Error handling
If an error occurs while processing an article, the script will print an error message and continue processing the remaining articles.
