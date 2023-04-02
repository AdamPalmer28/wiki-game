"""
Extracts data from exisiting wiki network data files growing the 
network and saving the new data to a new file.

data_content
url_name, n_out, headers, n_out_headers, n_in, in_url

"""

import pandas as pd
import asyncio
from wiki_network.wiki_page import artical_content
import testing.async_wiki.async_functions as af
import httpx

class wiki_network_data:

    def __init__(self):

        self.data = pd.read_csv('data/data_content.csv')

        self.save_increment = 1000 # save every x pages
        self.save_count = 0

    def run_extract(self, start_lst):
        """
        Run the data extraction
        """
        pass

    async def extract(self, lst):
        """
        Extract data from a list of urls
        """
        async with httpx.AsyncClient() as client:
            tasks = [self.get_page_links(url, client) for url in url_set]

            responses = await asyncio.gather(*tasks)
            all_links = set([item for sublist in responses for item in sublist])

            # add links to new links
            new_links.update(all_links)

        