import requests
import httpx

from bs4 import BeautifulSoup
import asyncio
import time


# Simple example

async def main():
    print("start")

    task = asyncio.create_task(wait(1))
    task2 = asyncio.create_task(wait(2))

    await task
    await task2

async def wait(txt):
    print(txt)
    await asyncio.sleep(1)
    print(f"{txt} - finished")


#asyncio.run(main())

# =============================================================================
# wiki links extract
# =============================================================================

def links_extract(content):
    "Extract all the links from the wiki page content"
    # Find all the <a> tags in the HTML and extract the links
    mainbody = content.find('div', id="bodyContent")

    links = []
    for link in mainbody.find_all('a'):
        href = link.get('href')
        if (href is not None) and (href.startswith('/wiki/')):
            href = 'https://en.wikipedia.org' + href
            links.append(href)

    return links


# =============================================================================
# async wiki extract
# =============================================================================

url_lst = ['https://en.wikipedia.org/wiki/Python_(programming_language)',
            'https://en.wikipedia.org/wiki/Wikipedia:Protection_policy#semi',
            'https://en.wikipedia.org/wiki/File:Python-logo-notext.svg',
            'https://en.wikipedia.org/wiki/Programming_paradigm',
            'https://en.wikipedia.org/wiki/Multi-paradigm_programming_language',
            'https://en.wikipedia.org/wiki/Object-oriented_programming',
            'https://en.wikipedia.org/wiki/Procedural_programming',
            'https://en.wikipedia.org/wiki/Imperative_programming',
            'https://en.wikipedia.org/wiki/Functional_programming',
            'https://en.wikipedia.org/wiki/Structured_programming',
            'https://en.wikipedia.org/wiki/Reflective_programming']

async def get_page_links(url, client):
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

        return links

async def async_links(lst):
    print("start")
    
    async with httpx.AsyncClient() as client:
        tasks = [get_page_links(url, client) for url in lst]

        responses = await asyncio.gather(*tasks)

        all_links = set([item for sublist in responses for item in sublist])
        print("Number of links: ", len(all_links))
              

    print("finished")


start1 = time.time()
asyncio.run(async_links(url_lst))
print(f"asyncio - {time.time() - start1} seconds")

# =============================================================================
# sync wiki extract
# =============================================================================

def sync_links(lst):
    print("start")

    for url in lst:
        response = httpx.get(url)

    print("finished")

start2 = time.time()
sync_links(url_lst)
print(f"sync - {time.time() - start2} seconds")

