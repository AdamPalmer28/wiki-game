"""
Wikipedia game
--------------

Summary: starting from a start wikipedia page, find a path to selected end 
wikipedia page only by clicking on links in the page article.

Objective:  (2 ways to play)
    - Find the shortest path between two wikipedia pages
    - Get to the end page quickest

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

        self.fwd_search = fwd_search(set([start_url]), end_url)
        self.lk_search = lk_search(set([end_url]))

        # Run game
        self.run()

    def run(self):
        """
        Main algorithm to find the path from start_url to end_url
        """
        while self.fwd_search.depth <= self.max_steps:
            
            # increase depth of general tree
            self.fwd_search.increase_depth()

            if 3 * self.lk_search.depth < self.fwd_search.depth:

                # increase depth of lk tree
                self.lk_search.increase_depth()

            if self.end_url in self.fwd_search.next_links:
                # exit
                print("Done")
                return
            
            #print(f"\nFound {self.found} links so far")
            print(f"Depth: {self.fwd_search.depth}, Visited tree: {len(self.fwd_search.tree)}")
            print(f"lk depth: {self.lk_search.depth}, lk visited tree: {len(self.lk_search.tree)}")


            
        
        return print(f"no path found in {self.max_steps} steps")




if __name__ == "__main__":

    start_url = "Python_(programming_language)"
    end_url = "Computer_performance"


    game = wiki_game(start_url, end_url, max_steps = 10)
    
