from link_handler import wiki_links
import asyncio


class fwd_search(wiki_links):

    def __init__(self, url_set, end_url: str):
        super().__init__(url_set)

        self.fwd_search = True

        self.end_url = end_url

        self.path = {}

    def increase_depth(self):
        """
        Increase depth by 1 of the general tree
        """

        new_links = asyncio.run(self.search_links(self.next_links))
        self.tree.update(self.next_links) # update visited tree

        self.next_links = new_links - self.tree # update next links


        self.depth += 1
    # =========================================================================
    #       Functions called once solution is found
    # =========================================================================
    def get_path(self, url):
        """
        Extract the exact path -
        After solution is found this function is called to extract the path
        """
        #path = [self.start_url]
        path = [url]

        def search_nested_dict(dict_value: dict):
            for key, value in dict_value.items():

                if isinstance(value, list):
                    # end depth
                    if url in value:
                        # end url found
                        path.append(key)
                        return True
                    
                
                elif isinstance(value, dict):
                    # search nested dict
                    result = search_nested_dict(value)

                    if result:
                        path.append(key)
                        return True
            return False
        
        search_nested_dict(self.path)
        return path[::-1]