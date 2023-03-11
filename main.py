"""
Wikipedia game
--------------

Summary: starting from a start wikipedia page, find a path to selected end 
wikipedia page only by clicking on links in the page article.

Objective:  (2 ways to play)
    - Find the shortest path between two wikipedia pages
    - Get to the end page quickest

"""

"""
TODO:

- filter down the wiki page to just articles
- learn how to use async
- learn how to use httpx (async requests)
"""

import requests
import httpx

from bs4 import BeautifulSoup
import asyncio
import time

class wiki_game:
    """
    Wiki game class
    """
    def __init__(self, start_url : str, end_url : str, max_steps : int  = 10):

        # function parameters
        self.start_url = start_url
        self.end_url = end_url
        self.max_steps = max_steps

        # temp 
        self.found = 0

        # Variable setup
        self.var_set_up()

        # Run game
        self.run()

    def run(self):
        """
        Main algorithm to find the path from start_url to end_url
        """
        while self.lk_depth <= self.max_steps:
            
            # increase depth of general tree
            self.increase_depth()

            if 3 * self.lk_depth < self.depth:

                # increase depth of lk tree
                self.increase_lk_depth()
  

            if self.end_url in self.next_links:
                print(f"Path found! {self.depth} steps, (I searched {self.found} pages)")
                path = self.get_path(self.end_url)
                return print(f"Path: {path}")
            
            # check if lk tree has found a 
            # local_links = self.lk_next_links.intersection(self.next_links)
            # if local_links:
            #     # priority next search
            #     self.next_links = local_links
            #     pass

            
            print(f"\nFound {self.found} pages so far")
            print(f"Depth: {self.depth}, Visited tree: {len(self.visited_tree)}")
            print(f"lk depth: {self.lk_depth}, lk visited tree: {len(self.lk_visited_tree)}")
            
        
        return print(f"no path found in {self.max_steps} steps")


    def increase_depth(self):
        """
        Increase depth by 1 of the general tree
        """

        print(len(self.next_links))
        print("Search")
        new_links = asyncio.run(self.search_links(self.next_links))
        self.visited_tree.update(self.next_links) # update visited tree

        #print(new_links)

        self.next_links = new_links - self.visited_tree # update next links

        print(len(self.next_links))

        self.depth += 1

    def increase_lk_depth(self):
        """
        Increase depth by 1 of the local knowledge tree
        """
        print("LK search")
        new_links = asyncio.run(self.search_links(self.lk_next_links))
        self.lk_visited_tree.update(self.lk_next_links) # update visited tree

        self.lk_next_links = new_links - self.lk_visited_tree # update next links


        self.lk_depth += 1


    # =========================================================================
    #       Depth / page searcher (need async)
    # =========================================================================
    
    async def search_links(self, url_set):
        """
        Search for links from a set of urls 
            Calls get_page_links to get all links from a single url
        """
        new_links = set()

        print(f"{len(url_set)}")
        
        async with httpx.AsyncClient() as client:
            tasks = [self.get_page_links(url, client) for url in url_set]

            responses = await asyncio.gather(*tasks)

            all_links = set([item for sublist in responses for item in sublist])

            # add links to new links
            new_links.update(all_links)


        self.found += len(url_set) 
        return new_links

    # Individual page searcher
    # =========================================================================
    async def get_page_links(self, url, client):
        """
        Get all links from a given url/page
        """

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
                href = 'https://en.wikipedia.org' + href
                links.append(href)

        #print(f"Found {len(links)} links from {url}")
        return links
    

    # =========================================================================
    #       Functions called once solution is found
    # =========================================================================
    def get_path(self, url):
        """
        Extract the exact path -
        After solution is found this function is called to extract the path
        """
        #path = [self.start_url]
        path = [self.end_url]

        def search_nested_dict(dict_value):
            for key, value in dict_value.items():
                if value == url:
                    # end url found
                    path.append(key)
                    return True
                
                if isinstance(value, dict):
                    # search nested dict
                    result = search_nested_dict(value)

                    if result:
                        path.append(key)
                        return True
            return False
        
        search_nested_dict(self.path)
        return path[::-1]
    
    def var_set_up(self):
        # --------------
        # Variable setup
        # --------------

        # tree - tree from start_url
        self.visited_tree = set()
        self.next_links = set([self.start_url]) # links to be visited next
        self.depth = 0
         
        # lk tree - "local knowledge" tree from end_url 
        self.lk_visited_tree = set()
        self.lk_next_links = set([self.end_url]) # links to be visited next
        self.lk_depth = 0

        # path
        self.path = []


if __name__ == "__main__":

    start_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    end_url = "https://en.wikipedia.org/wiki/Computer_performance"

    game = wiki_game(start_url, end_url, max_steps = 10)

    
