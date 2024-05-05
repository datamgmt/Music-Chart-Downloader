"""

scrape_to_csv.py by David M Walker

A utility to scrape the weekly chart data from the files downloaded by download_html.py
Each .html file is read and an equivalent .csv file is created. A file called all_data.csv
is created that has the data from all the source files in a single file.

"""

# pylint: disable=C0301

import glob
import csv
import os
from bs4 import BeautifulSoup

OUTPUT_DIR = "data/csv/"
INPUT_FILES = "data/html/*.html"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

ALL_DATA_FILE = OUTPUT_DIR + "all_data.csv"

with open(ALL_DATA_FILE, 'w', newline='', encoding="utf-8") as all_csvfile:

    fieldnames = ['chart_date', 'chart_position', 'chart_artist',
                 'chart_title', 'chart_movement', 'chart_peak', 'chart_weeks']
    all_writer = csv.DictWriter(all_csvfile, fieldnames=fieldnames, lineterminator=os.linesep)
    all_writer.writeheader()

    for path in sorted(glob.glob(INPUT_FILES)):

        print(path)

        this_data_file = OUTPUT_DIR + path.split('/')[-1].split('.')[0] + ".csv"

        with open(this_data_file, 'w', newline='', encoding="utf-8") as this_csvfile:

            this_writer = csv.DictWriter(this_csvfile, fieldnames=fieldnames,
                lineterminator=os.linesep)
            this_writer.writeheader()

            with open(path, "r", encoding="utf-8") as file:

                soup = BeautifulSoup(file.read(), 'html.parser')

                chart_date_data = soup.select("div.prose span.sr-only")[0].text.split(" on ")[1]
                CHART_DATE = f"{int(chart_date_data.split('/')[2]):04d}-{int(chart_date_data.split('/')[1]):02d}-{int(chart_date_data.split('/')[0]):02d}"

                #rows = [row for row in soup.select("div.chart-item") ]
                rows = list(soup.select("div.chart-item"))

                for row in rows:

                    CHART_POSITION = ""
                    CHART_ARTIST = ""
                    CHART_TITLE = ""
                    CHART_MOVEMENT = "New"
                    CHART_PEAK = ""
                    CHART_WEEKS = ""

                    if len(row.select("div.chart-item-content div.position strong") ):
                        CHART_POSITION = row.select("div.chart-item-content div.position strong")[0].text

                    if len(row.select("a.chart-artist span")):
                        CHART_ARTIST = row.select("a.chart-artist span")[0].text

                    if len(row.select("a.chart-name span")):
                    # Specifically to deal with 14 Nv 1952 - first ever chart
                        if len(row.select("a.chart-name span"))==1:
                            CHART_TITLE = row.select("a.chart-name span")[0].text
                        else:
                            CHART_TITLE = row.select("a.chart-name span")[1].text

                    if len(row.select("li.movement span")):
                        CHART_MOVEMENT = row.select("li.movement span")[1].text

                    if len(row.select("li.peak span")):
                        CHART_PEAK = row.select("li.peak span")[0].text

                    if len(row.select("li.weeks span")):
                        CHART_WEEKS = row.select("li.weeks span")[0].text

                    if len(CHART_POSITION) > 0:
                        all_writer.writerow({'chart_date': CHART_DATE,
                                             'chart_position': CHART_POSITION,
                                             'chart_artist': CHART_ARTIST,
                                             'chart_title': CHART_TITLE, 
                                             'chart_movement': CHART_MOVEMENT,
                                             'chart_peak': CHART_PEAK, 
                                             'chart_weeks': CHART_WEEKS})
                        this_writer.writerow({'chart_date': CHART_DATE,
                                              'chart_position': CHART_POSITION,
                                              'chart_artist': CHART_ARTIST, 
                                              'chart_title': CHART_TITLE, 
                                              'chart_movement': CHART_MOVEMENT, 
                                              'chart_peak': CHART_PEAK, 
                                              'chart_weeks': CHART_WEEKS})

print ("Finished")
