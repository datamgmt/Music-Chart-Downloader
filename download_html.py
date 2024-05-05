"""

download_html.py by David M Walker

A utility to download the weekly chart data from 14-Nov-1952 to date and store 
them for later processing. If a .html file already exists then no attempt is made
to download it. 

"""

import datetime
from datetime import date
import os
import requests

def download_file(url):
    """ Function to download the file for a given week """
    local_filename = f"{OUTPUT_DIR}{url.strip('/').split('/')[-1]}.html"
    if not os.path.exists(local_filename):
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    return local_filename

today = date.today()
fetch_date = datetime.date(1952,11,14)
OUTPUT_DIR = "data/html/"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

while fetch_date < today:
    page = f"https://www.officialcharts.com/charts/singles-chart/{fetch_date.strftime('%Y%m%d')}"
    print (page)
    download_file(page)
    fetch_date = fetch_date + datetime.timedelta(7)

print ("Finished")
