from link_handler import wiki_links
import asyncio

class lk_search(wiki_links):

    def __init__(self, url_set=set()):
        super().__init__(url_set)

        self.path = {}

    def increase_depth(self):
        """
        Increase depth by 1 of the local knowledge tree
        """
        new_links = asyncio.run(self.search_links(self.next_links))
        self.tree.update(self.next_links) # update visited tree

        self.next_links = new_links - self.tree # update next links


        self.depth += 1

    def get_prefence(self, fwd_search):
        
        pass