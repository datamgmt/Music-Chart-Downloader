# uk-chart-data

Download UK Chart Data from OfficialCharts.com

The objective is to download the UK charts from https://www.officialcharts.com

The UK Official Charts does not make it easy to download the raw data
&nbsp;musc
* download_charts.py that downloads the charts into a directory raw/charts/YYYYMMDD
* scrape.py that converts the file and extracts the chart positions and enhances it with Spotify data

download_charts.py works and downloads all the files from 14 November 1952 to 26 April 2024 (3729 weeks in total)
This means polling the site just once and storing them rather than repeatedly going back and getting blocked

In the early days of the charts it was a Top 12, expanding to 20, 30, 50, 75 and currently Top 100 singles

For the scrape.py there are several changes

* The Spotify data if not needed as it is being merged into a better Discogs data set
* Since the original script there have been format changes on the website and they have removed some of the DIV tags names that made scraping easier
* As a result of the change in format all the previous projects on the web have been depreciated

The objective is to create a json object or a csv file with the following fields

* chart_date e.g. 11-01-2019
* chart_position e.g. 1
* title e.g. SWEET BUT PSYCHO
* artist e.g. AVA MAX
* position_last_week e.g. 1
* peak_position e.g. 1
* weeks_in_chart e.g. 12

Example

I have used the data for 11-Jan-2019

https://www.officialcharts.com/charts/singles-chart/20190111/7501/

The datafile is in Examples/20190111

I have stripted all the tags except for DIV to find the key attripbutes
These are in Examples/20190111-divs.txt

The #1 record is in a class "primis chart-item relative text-right"
The #2-#100 records are in a class "chart-item relative text-right"

The complete subset of the #1 and #2 of 11-Jan-2019 with all tags is in 20190111-subset.txt



