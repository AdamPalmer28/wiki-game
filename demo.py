import requests
from bs4 import BeautifulSoup

# Make a GET request to the webpage
url = 'https://www.example.com'
response = requests.get(url)

# Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the <a> tags in the HTML and extract the links
links = []
for link in soup.find_all('a'):
    href = link.get('href')
    if href is not None:
        links.append(href)

# Print the list of links
print('List of links: ')
print(links)

