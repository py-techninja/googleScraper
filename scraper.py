#scrape google
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
import trafilatura as Reader


class Search:
    def __init__(self, query):
        self.query = query
        self.url = "https://www.google.com/search?q=" + query
        self.response = self.get_results()
    
    def get_results(self):
        url = self.url
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
            raise Exception(e)    

    def related_links(self):
        response = self.response
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
    
    def results(self):
        query = self.query
        url = self.url
        response = self.response
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
            text = result.text.split('\nSearch for:')[0]
            self.query = text
            self.url = "https://www.google.com/search?q=" + text
            self.response = self.get_results()
            try:
                content = self.response.html.find(css_identifier_result)[0]
                content = content.find(css_identifier_text, first=True).text
            except:
                content = ''
                
            item = {
                'text': text,
                'content': content
            }

            related.append(item)

            self.query = query
            self.url = url
            self.response = response
        
        return {'output': output, 'related': related, 'links': self.related_links()}
        
    def content(self, link):
        content = Reader.fetch_url(link)
        content = Reader.extract(content, include_tables=False, include_comments=False)
        return content



query = "reverse a list in python"
search = Search(query)
results = search.results()# => {[{ouput}], [{related}], [{links}]}

print('Main Content')
for result in results['output']:
    title = result['title']
    text = result['text']
    link = result['link'] 
    full_text = search.content(link)
    print(text)
    
print('\n\n')


print('Related Content')
for related in results['related']:
    text = related['text']
    content = related['content']
    print(related)
    
print('\n\n')

print('Related Links')
print(results['links'])
     

#scrape_google => list(links)

#goole_search => top search => [{top result}, {related search}]

