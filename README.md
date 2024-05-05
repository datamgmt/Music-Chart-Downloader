# uk-chart-data

Download UK Chart Data from OfficialCharts.com

The objective is to download the UK charts from https://www.officialcharts.com

The UK Official Charts does not make it easy to download the raw data, there is no API so scapring every page is the only way

In the early days of the charts it was a Top 12, expanding to 20, 30, 50, 75 and currently Top 100 singles

There are two scripts in this folder

= download_charts.py =

* download_charts.py downloads the charts into a directory data/html/YYYYMMDD.html
* It downloads all the files from 14 November 1952 to the latest chart
* If a chart already exists it skips that week and moves on to the next week - this means that used repeatedly it will minimise the fetches to the missing charts only
* There are 3730 charts to May 2024

= scrape_to_csv.py =

* scrape_to_csv.py that converts all the files in data/html and writes a file per day in data/html/YYYYMMDD.csv 
* It also creates a file with the data from all the .html files in data/csv/all_data.csv

= Output format =

* chart_date e.g. 2024-02-26
* chart_position e.g. 1
* chart_artist e.g. AVA MAX
* chart_title e.g. SWEET BUT PSYCHO
* chart_movement e.g. 1
* chart_peak e.g. 1
* chart_weeks e.g. 12


This utility was written on an Apple M1 Ultra based Mac running Sonoma 14.4.1 and Python version 3.9.6 
Written and tested on 5 May 2024 - note that data formats of the source may vary over time
This code is unmaintained