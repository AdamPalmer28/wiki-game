"""
Python parent class for handling links
"""
from bs4 import BeautifulSoup
import asyncio
import time
import httpx

class wiki_links:
    "Wiki links class for handling all links"

    def __init__(self, url_set = set()):

        self.url_set = url_set
        
        self.depth = 0

    async def search_links(self, url_set, fwd_search = False):
        """
        Search for links from a set of urls 
            Calls get_page_links to get all links from a single url
        """
        new_links = set()

        print(f"{'Normal depth' if fwd_search else 'LK depth'}: {len(url_set)}")
        
        async with httpx.AsyncClient() as client:
            tasks = [self.get_page_links(url, client, fwd_search) for url in url_set]

            responses = await asyncio.gather(*tasks)

            all_links = set([item for sublist in responses for item in sublist])

            # add links to new links
            new_links.update(all_links)

        return new_links

    # Individual page searcher
    # =========================================================================
    async def get_page_links(self, url, client, fwd_search = False):
        """
        Get all links from a given url/page
        """
        url = 'https://en.wikipedia.org/wiki/' + url
        response = await client.get(url)

        # Use BeautifulSoup to parse the HTML content
        content = BeautifulSoup(response.content, 'html.parser')
        
        mainbody = content.find('div', id="bodyContent")
        if mainbody is None:
            return []
        
        links = []
        for link in mainbody.find_all('a'):
            href = link.get('href')

            if (href is not None) and (href.startswith('/wiki/')):
                href =  href.replace('/wiki/', '') # remove repeative url links
                links.append(href)

        self.found += len(links) # links found

        if fwd_search:
            if self.end_url in links:
                    print(f"Path found! {self.depth + 1} steps, (I found {self.found} wiki links)")
                    print(f"total time: {time.time() - self.time_start} seconds")
                    path = self.get_path(self.end_url)
                    print(f"Path: {path}")

        return links