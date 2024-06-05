import logging
import os
import hydra
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def download(url, out_dir):
    """
    Download the latest release of Lexicon in XML with the URL retrieved from find_latest_release function
    and save it in the out_dir directory.
    """
    response = requests.get(url) # send a GET request to the URL
    local_path = os.path.join(out_dir, 'LEXICON.xml') # save the file as LEXICON.xml
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'html.parser')
        list_items = soup.find_all('li')
        for li in list_items:
            a_tag = li.find('a')
            if a_tag and 'href' in a_tag.attrs:
                href = a_tag['href']
                if href.endswith('.xml'): # download the XML file
                    LOGGER.info(f"Downloading {href}...")
                    headers = {'User-Agent': 'Mozilla'} # add a user agent to avoid 403 Forbidden error
                    response = requests.get(href, headers=headers)
                    if response.status_code == 200:
                        with open(local_path, 'wb') as f: # save the file in the out_dir directory
                            f.write(response.content)
                        LOGGER.info(f"Downloaded the file to {local_path}")
                    else:
                        msg = f"Failed to download {href}"
                        LOGGER.error(msg)
                        raise Exception(msg)
                    return
    else:
        msg = f"Failed to download from {url}"
        LOGGER.error(msg)
        raise Exception(msg)



def find_latest_release(base_url, index_url):
    """
    Find the latest release of Lexicon. 
    """
    LOGGER.info('Finding the latest release of Lexicon...')
    response = requests.get(base_url) # send a GET request to the base URL
    
    #Parse the HTML content and find the latest release by comparing the years
    if response.status_code == 200: # check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser') # parse the HTML content
        list_items = soup.find_all('li') # find all list items
        max_year = -1 # initialize the maximum year
        latest_release = None # initialize the latest release
        for li in list_items: # iterate over the list items to find the latest release
            a_tag = li.find('a') # find the anchor tag
            if a_tag and 'href' in a_tag.attrs: # check if the anchor tag has an href attribute
                href = a_tag['href'] # get the href attribute
                text = a_tag.get_text(strip=True) # get the text content of the anchor tag
                if "Lexicon Release" in text: # if the text contains "Lexicon Release" then extract the year
                    year = int(text.split()[0])
                    if year > max_year:
                        max_year = year
                        latest_release = href
                        
        if latest_release: # check if the latest release is found
            LOGGER.info(f"Found the latest release: {latest_release}")
            if not latest_release.startswith('http'): # data before 2020 and after 2020 have different URL formats, so here is a fix for that
                latest_release = urljoin(base_url, latest_release) 
            LOGGER.info(f"Downloading the latest release from {latest_release}")
            return latest_release # return the latest release URL
        else:
            msg = "No relevant Lexicon Release found."
            LOGGER.error(msg)
            raise Exception(msg)
                
    else:
        msg = f"Failed to retrieve data from{index_url}"
        LOGGER.error(msg)
        raise Exception(msg)

@hydra.main(config_path="./conf", config_name="config", version_base=None)
def main(cfg):
    """
    Automated download tool: write a script to download the latest release of Lexicon automatically: 
    https://lhncbc.nlm.nih.gov/LSG/Projects/lexicon/current/web/release/index.html. 
    """
    base_url = "https://lhncbc.nlm.nih.gov/LSG/Projects/lexicon/current/web/release/" # base URL
    index_url = urljoin(base_url, 'index.html') # index URL
    out_dir = cfg.download.out_dir # output directory
    latest_release = find_latest_release(base_url, index_url) # find the latest release
    #check if out_dir exists if not create it
    if not os.path.exists(out_dir):
        LOGGER.info(f"Creating directory {out_dir}")
        os.makedirs(out_dir)
    download(latest_release, out_dir) # download the latest release



if __name__ == '__main__':
    main()