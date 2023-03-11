import requests
from bs4 import BeautifulSoup
import asyncio

class wiki_game:
    def __init__(self, start_url, end_url, max_steps=10):

        self.start_url = start_url
        self.end_url = end_url
        self.max_steps = max_steps

        # tree - tree from start_url
        self.visited_tree = set()
        self.next_links = set([start_url]) # links to be visited next
        self.depth = 0
         
        # lk tree - "local knowledge" tree from end_url 
        self.lk_visited_tree = set()
        self.lk_next_links = set([end_url])
        self.lk_depth = 0

        # path
        self.path = []

    def run(self):
        """
        Main algorithm to find the path from start_url to end_url
        """
        while self.lk_depth < self.max_steps:


            
            # increase depth of general tree
            self.increase_depth()

            if self.lk_depth < 3 * self.depth:

                # increase depth of lk tree
                self.increase_lk_depth()
  

            if self.end_url in self.next_links:
                print(f"Path found! {self.depth} steps, (I searched {len(self.visited_tree)} pages)")
                path = self.get_path(self.end_url)
                return print(f"Path: {path}")
            
            # check if lk tree has found a 
            local_links = self.lk_next_links.intersection(self.next_links)
            if local_links:
                # priority next search
                self.next_links = local_links
                pass
        
        return print(f"no path found in {self.max_steps} steps")


    def increase_depth(self):
        """
        Increase depth by 1 of the general tree
        """
        new_links = self.search_links(self.next_links)
        self.next_links = new_links - self.visited_tree

        self.depth += 1

    def increase_lk_depth(self):
        """
        Increase depth by 1 of the local knowledge tree
        """
        new_links = self.search_links(self.lk_next_links)

        self.lk_next_links = new_links - self.lk_visited_tree
        


        self.lk_depth += 1

    def get_path(self, url):
        "find end path"
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

    # =========================================================================
    #       Depth / page searcher
    # =========================================================================
    
    def search_links(self, url_set):
        """
        Search for links from a set of urls 
            Calls get_page_links to get all links from a single url
        """
        new_links = set()
        for link in url_set:
            # overall visited tree
            self.visited_tree.add(link)

            # get links from link
            links = self.get_page_links(link)

            # add links to new links
            new_links.update(links)

        return new_links

    # Individual page searcher
    # =========================================================================
    async def get_page_links(self, url):
        """
        Get all links from a given url/page
        """
        # Make a GET request to the webpage
        response = requests.get(url)

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the <a> tags in the HTML and extract the links
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None:
                links.append(href)

        return links