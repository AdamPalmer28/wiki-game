"""
This module contains the class for a wiki page.

This class is used to extract the content from a wiki page.
"""

class artical_content:
    """
    Extract the content from a wiki page
    """

    def __init__(self, content, wiki_url: str):

        self.get_artical(content) # filter page content

        self.wiki_url = wiki_url

    def get_links(self):
        """
        Get all links from page content
        """
        pass

    def get_headers(self):
        """
        Get all headers from the wiki artical
        With the associated links of each section/header
        """
        pass

    def summarise(self):
        """
        Summarise the page content into key words for 
        """
        pass

    def get_artical(self, content):
        """
        Get the artical from wiki page, removing all irrelevant html
        elements which are not going to yeild any useful information
        """
        # id = "mw-content-text"
