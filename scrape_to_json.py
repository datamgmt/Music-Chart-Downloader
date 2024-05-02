# Not yet converted from scrape_to_csv

from bs4 import BeautifulSoup
import glob
import json
import base64
import os

output_dir = "data/json/"
input_files = "data/html/*.html"

if not os.path.exists(output_dir):
   os.makedirs(output_dir)
   
all_data_file = output_dir + "all_data.json"
   
with open(all_data_file, 'w', newline='') as all_csvfile:
   
   fieldnames = ['chart_date', 'chart_position', 'chart_artist', 'chart_title', 'chart_movement', 'chart_peak', 'chart_weeks']
   all_writer = csv.DictWriter(all_csvfile, fieldnames=fieldnames, lineterminator=os.linesep)
   all_writer.writeheader()
    
   for path in sorted(glob.glob(input_files)):

     print(path)
       
     this_data_file = output_dir + path.split('/')[-1].split('.')[0] + ".json"

     with open(this_data_file, 'w', newline='') as this_csvfile:
      
        this_writer = csv.DictWriter(this_csvfile, fieldnames=fieldnames, lineterminator=os.linesep)
        this_writer.writeheader()

        with open(path, "r") as file:
            
           soup = BeautifulSoup(file.read(), 'html.parser')
            
           chart_date  = soup.select("div.prose span.sr-only")[0].text.split(" on ")[1]
            
           rows = [row for row in soup.select("div.chart-item") ]

           for row in rows:
               
              chart_position = ""
              chart_artist = ""
              chart_title = ""
              chart_movement = "New"
              chart_peak = ""
              chart_weeks = ""
                
              if len(row.select("div.chart-item-content div.position strong") ):
                 chart_position = row.select("div.chart-item-content div.position strong")[0].text
               
              if len(row.select("a.chart-artist span")):
                 chart_artist = row.select("a.chart-artist span")[0].text

              if len(row.select("a.chart-name span")):
                 # Specifically to deal with 14 Nv 1952 - first ever chart
                 if len(row.select("a.chart-name span"))==1:
                    chart_title = row.select("a.chart-name span")[0].text 
                 if len(row.select("a.chart-name span"))!=1:
                    chart_title = row.select("a.chart-name span")[1].text 
                    
              if len(row.select("li.movement span")):
                 chart_movement = row.select("li.movement span")[1].text

              if len(row.select("li.peak span")):
                 chart_peak = row.select("li.peak span")[0].text

              if len(row.select("li.weeks span")):
                 chart_weeks = row.select("li.weeks span")[0].text
                  
              if len(chart_position):
                 all_writer.writerow({'chart_date': chart_date, 'chart_position': chart_position, 'chart_artist': chart_artist, 'chart_title': chart_title, 'chart_movement': chart_movement, 'chart_peak': chart_peak, 'chart_weeks': chart_weeks})
                 this_writer.writerow({'chart_date': chart_date, 'chart_position': chart_position, 'chart_artist': chart_artist, 'chart_title': chart_title, 'chart_movement': chart_movement, 'chart_peak': chart_peak, 'chart_weeks': chart_weeks})

print ("Finished")
