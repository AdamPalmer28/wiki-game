import httpx
from bs4 import BeautifulSoup
import asyncio

async def get_page_links(url, client):
        """
        Get all links from a given url/page
        """
        url = 'https://en.wikipedia.org/wiki/' + url

        response = await client.get(url)

        # Use BeautifulSoup to parse the HTML content
        content = BeautifulSoup(response.content, 'html.parser')
        mainbody = content.find('div', id = "mw-content-text")
        #print(mainbody)

        if mainbody is None:
            return []
        
        links = []
        for link in mainbody.find_all('a'):
            href = link.get('href')
            if (href is not None) and (href.startswith('/wiki/')):
                if ':' in href: # remove special links
                    continue
                href =  href.replace('/wiki/', '') # remove repeative url links
                links.append(href)

        print(f"{url} Links found: {len(links)}")
        return links

async def async_links(lst):
    print("start")
    
    async with httpx.AsyncClient() as client:
        tasks = [get_page_links(url, client) for url in lst]

        responses = await asyncio.gather(*tasks)

        all_links = set([item for sublist in responses for item in sublist])

        # write to file
        with open('async/links.txt', 'w') as f:
            for link in all_links:
                f.write(link + '\n')
        

if __name__ == '__main__':
    url_lst = ['Structured_programming', 'United_States', 'Python_(programming_language)']
    
    asyncio.run(async_links(url_lst))