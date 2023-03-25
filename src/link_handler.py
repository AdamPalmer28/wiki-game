"""
Python parent class for handling links
"""
from bs4 import BeautifulSoup
import time
import httpx
import asyncio

class wiki_links:
    "Wiki links class for handling all links"

    def __init__(self, url_set = set()):

        #self.url_set = url_set
        self.next_links = url_set

        self.tree = set()
        self.current_branch = set()

        self.url_found = 0
        self.depth = 0
        self.fwd_search = False

    # =========================================================================
    #       Depth / page searcher (need async)
    # =========================================================================
    async def search_links(self, url_set):
        """
        Search for links from a set of urls 
            Calls get_page_links to get all links from a single url
        """
        new_links = set()

        async with httpx.AsyncClient() as client:
            tasks = [self.get_page_links(url, client) for url in url_set]

            responses = await asyncio.gather(*tasks)
            all_links = set([item for sublist in responses for item in sublist])

            # add links to new links
            new_links.update(all_links)

        return new_links

    # Individual page searcher
    # =========================================================================
    async def get_page_links(self, url, client):
        """
        Get all links from a given url/page
        """
        url = 'https://en.wikipedia.org/wiki/' + url
        response = await client.get(url)
        
        # Use BeautifulSoup to parse the HTML content
        content = BeautifulSoup(response.content, 'html.parser')
        mainbody = content.find('div', "mw-parser-output")

        if mainbody is None:
            return []
        
        links = []
        for link in mainbody.find_all('a'):
            href = link.get('href')

            if (href is not None) and (href.startswith('/wiki/')):
                href =  href.replace('/wiki/', '') # remove repeative url links
                links.append(href)

        self.url_found += len(links) # links found

        if self.fwd_search:
            if self.end_url in links:
                print(f"Path found! {self.depth + 1} steps, (I found {self.url_found} wiki links)")
                print(f"total time: {time.time() - self.time_start} seconds")

        return links