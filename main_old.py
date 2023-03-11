import requests
from bs4 import BeautifulSoup
import asyncio

async def get_links(url):
    """Return a list of links from the given URL."""
    # Make a GET request to the webpage
    response = await requests.get(url)

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <a> tags in the HTML and extract the links
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None:
            links.append(href)

    return links

def wiki_game(start_url, end_url, max_steps=10):
    """
    Find a path from start_url to end_url in at most max_steps steps.

    And then return the path by working backwards from the mid point back
    to the start_url and end_url.
    
    """
    
    # Create a queue of paths
    queue = [[start_url]]

    # Create a set of visited URLs
    s_visited_tree = set()
    e_visited_tree = set()

    # Create a set of current links
    s_cur_depth_links = set([start_url])
    e_cur_depth_links = set([end_url])
    s_depth, e_depth = 0, 0

    # while intersection of visited trees is empty
    path_not_found = True
    while path_not_found:
        s_new_links, e_new_links = set(), set()

        # search from start_url
        s_depth += 1
        for link in s_cur_depth_links:
            # overall visited tree
            s_visited_tree.add(link)

            # get links from link
            links = get_links(link)

            # add links to new links
            s_new_links.update(links)

        s_new_links = s_new_links - s_visited_tree
        
        if s_new_links.intersection(e_visited_tree):
            # path found
            break

        # search from end_url
        e_depth += 1
        for link in e_cur_depth_links:
            e_visited_tree.add(link)

            # get links from link
            links = get_links(link)

            # add links to new links
            e_new_links.update(links)

        if e_new_links.intersection(s_visited_tree):
            # path found
            break

        # No path found on this iteration
            # prepare for next iteration

        # update current links
        s_cur_depth_links = s_new_links
        e_cur_depth_links = e_new_links


        if s_depth + e_depth> max_steps:
            # early exit
            print(f'No path found in {max_steps} steps.')   
            return None


    