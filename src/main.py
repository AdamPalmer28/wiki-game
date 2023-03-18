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

import time
from fwd_search import fwd_search
from lk_search import lk_search

class wiki_game:
    """
    Wiki game class
    """
    def __init__(self, start_url : str, end_url : str, max_steps : int  = 10):

        # function parameters
        self.start_url = start_url
        self.end_url = end_url
        self.max_steps = max_steps

        self.time_start = time.time()

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
                # exit
                return
            
            print(f"\nFound {self.found} links so far")
            print(f"Depth: {self.depth}, Visited tree: {len(self.visited_tree)}")
            print(f"lk depth: {self.lk_depth}, lk visited tree: {len(self.lk_visited_tree)}")


            
        
        return print(f"no path found in {self.max_steps} steps")




if __name__ == "__main__":

    start_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    end_url = "https://en.wikipedia.org/wiki/Computer_performance"


    game = wiki_game(start_url, end_url, max_steps = 10)
    
