import datetime
from datetime import date
import os
import requests

def download_file(url):
   local_filename = f"{output_dir}{url.strip('/').split('/')[-1]}.html"
   if not os.path.exists(local_filename):
      with requests.get(url, stream=True) as r:
         r.raise_for_status()
         with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
               if chunk:
                  f.write(chunk)
   return local_filename

today = date.today()
fetch_date = datetime.date(1952,11,14)
output_dir = "data/html/"

if not os.path.exists(output_dir):
   os.makedirs(output_dir)

while fetch_date < today:
   page = f"https://www.officialcharts.com/charts/singles-chart/{fetch_date.strftime('%Y%m%d')}"
   print (page)
   download_file(page)
   fetch_date = fetch_date + datetime.timedelta(7)

print ("Finished")