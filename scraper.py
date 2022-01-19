#scrape google
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import trafilatura as Reader



def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    
    return response

def parse_results(response):
    
    css_identifier_result = ".hlcw0c" #".yuRUbf" #"jtfYYd"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".NJo7tc.Z26q7c.uUuwM" #"VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc.lEBKkf"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    #get top results
    for result in results:
        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            'text': result.find(css_identifier_text, first=True).text
        }
        
        output.append(item)

    #get related tags
    related = []
    
    css_identifier_related = '.wQiwMc.ygGdYd.related-question-pair'
    
    results = response.html.find(css_identifier_related)
    for result in results:
        item = {
            'text': result.text.split('\nSearch for:')[0]
        }

        related.append(item)
    
    return {'output': output, 'related': related}

def google_search(query):
    response = get_results(query)
    return parse_results(response)




def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

        
def scrape_google(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

def content(link):
    content = Reader.fetch_url(link)
    content = Reader.extract(content, include_tables=False, include_comments=False)
    return content


query = "reverse a list in python"

links = scrape_google(query) #=> [ links ] related to the search
for link in links:
    print(content(link))
    

results = google_search(query) # => [{ouput}, {related}]

for result in results['output']:
    title = result['title']
    text = result['text']
    link = result['link'] 
    full_text = content(link)
    print(full_text)

for related in results['related']:
    related = related['text']
    links = scrape_google(related)
    print(links)

    results = google_search(related)
    print(results)

print('done')

#scrape_google => list(links)

#goole_search => top search => [{top result}, {related search}]

