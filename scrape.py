from bs4 import BeautifulSoup
import glob
import csv
import base64
import os

with open('import/items.csv', 'w', newline='') as csvfile:
   
    fieldnames = ['chart_date', 'chart_position', 'chart_artist', 'chart_title', 'chart_movement', 'chart_peak', 'chart_weeks']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for path in glob.glob("raw/charts/*"):
        with open(path, "r") as file:
            print(path)
            
            
            soup = BeautifulSoup(file.read(), 'html.parser')
            
            chart_date  = soup.select("div.prose span.sr-only")[0].text.split(" on ")[1]
            
            rows = [row for row in soup.select("div.chart-item") ]

            for row in rows:
               
               chart_position = ""
               chart_artist = ""
               chart_title = ""
               chart_movement = ""
               chart_peak = ""
               chart_weeks = ""
                
               if len(row.select("div.chart-item-content div.position strong") ):
                  chart_position = row.select("div.chart-item-content div.position strong")[0].text
               
               if len(row.select("a.chart-artist span")):
                  chart_artist = row.select("a.chart-artist span")[0].text

               if len(row.select("a.chart-name span")):
                  chart_title = row.select("a.chart-name span")[1].text
            
               if len(row.select("li.movement span")):
                  chart_movement = row.select("li.movement span")[1].text

               if len(row.select("li.peak span")):
                  chart_peak = row.select("li.peak span")[0].text

               if len(row.select("li.weeks span")):
                  chart_weeks = row.select("li.weeks span")[0].text
                  
               if len(chart_position):
                  writer.writerow({'chart_date': chart_date, 'chart_position': chart_position, 'chart_artist': chart_artist, 'chart_title': chart_title, 'chart_movement': chart_movement, 'chart_peak': chart_peak, 'chart_weeks': chart_weeks})
