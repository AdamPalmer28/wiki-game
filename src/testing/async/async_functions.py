import asyncio
import httpx

__all__ = ['gather_links']

async def gather_links(url_set):
    """
    Search for links from a set of urls 
        Calls get_page_links to get all links from a single url
    """

    async with httpx.AsyncClient() as client:
        tasks = [get_page_links(url, client) for url in url_set]

        responses = await asyncio.gather(*tasks)
        #all_links = set([item for sublist in responses for item in sublist])

    return 


# later will replace this with wiki_network.wiki_page
async def get_page_links(url, client):

    url = 'https://en.wikipedia.org/wiki/' + url
    try:
        response = await client.get(url)
    except:# need to make better error handling
        print(f"Error: {url}")

        return 
    return
