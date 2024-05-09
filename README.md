# Music Chart Downloader

Music Chart Downloader (mcd.py) by David M Walker

(c) 2024 Data Management & Warehousing

Extract chart data from chart websites and store in files

Currently supports OfficialCharts.com Singles & Albums charts

## Overview

* This utility downloads the charts in html format from OfficialCharts.com (https://www.officialcharts.com)
* The script can download the UK Singles Chart or the UK Album Chart.
* The download can be for a single week, a range of weeks or all historical charts.
* It then writes out the data as either a json file or a csv file for use elsewhere.

## Process

* Download all the html files for the data range requested from the chart website
* html files that have already been downloaded will not be re-downloaded
* Parse the files for the chart entries
* Write the files out in either a json or csv file 
* Charts can be written out as one file per week or one file for all data

## Running the script

Download all UK Singles charts and create a single CSV file with all the data
```
./mcd.py
```

Download the 2023 UK Album charts and write one JSON file per week

```
./mcd.py --chart uk-albums --startdate 20230101 --enddate 20231231 --output_type json --output_set weekly
```

Help and options

```
usage: mcdc.py [-h] [--chart {uk-singles,uk-albums}] [--startdate STARTDATE] [--enddate ENDDATE] [--datadir DATADIR]
               [--output_type [{csv,json} ...]] [--output_set [{weekly,all} ...]]

The Music Chart Data Collector

optional arguments:
  -h, --help            show this help message and exit
  --chart {uk-singles,uk-albums}
                        Which music chart to download, (Default: uk-singles)
  --startdate STARTDATE
                        The first chart to download in YYYYMMDD format (Default: 19521114)
  --enddate ENDDATE     The last chart to download in YYYYMMDD format (Default: 20240509)
  --datadir DATADIR     Location of datafiles used in processing (Default: ./data)
  --output_type [{csv,json} ...]
                        Output file formats required (Default: ['csv'])
  --output_set [{weekly,all} ...]
                        Weekly charts and/or one large file (Default: ['all'])

(c)2024 Data Management & Warehousing
```

## Directory Structure

```
.
├── README.md                   # This file
├── data                        # Data Firectories
│   ├── csv                     # CSV Output files
│   ├── html                    # Downloaded HTML Files
│   └── json                    # JSON Output files
├── mcdc.py                     # The script
└── samples                     # sample html files to understand the structure 
    ├── uk-singles-chart.html
    └── uk-singles-chart.png

```

## Available data field

* chart_date e.g. 2024-04-26
* chart_position e.g. 1
* chart_artist e.g. AVA MAX
* chart_title e.g. SWEET BUT PSYCHO
* chart_movement e.g. 1
* chart_peak e.g. 1
* chart_weeks e.g. 12

## CSV Format example

```
chart_date,chart_position,chart_artist,chart_title,chart_movement,chart_peak,chart_weeks
19521114,1,AL MARTINO,HERE IN MY HEART,New,1,1
19521114,2,JO STAFFORD,YOU BELONG TO ME,New,2,1
19521114,3,NAT 'KING' COLE,SOMEWHERE ALONG THE WAY,New,3,1
19521114,4,BING CROSBY,THE ISLE OF INNISFREE,New,4,1
19521114,5,GUY MITCHELL,FEET UP (PAT HIM ON THE PO-PO),New,5,1
19521114,6,ROSEMARY CLOONEY,HALF AS MUCH,New,6,1
```

## JSON Format example

```
[
    {
        "chart_date": "20221230",
        "chart_movement": "3",
        "chart_position": "1",
        "chart_artist": "MICHAEL BUBLE",
        "chart_title": "CHRISTMAS",
        "chart_peak": "1",
        "chart_weeks": "105"
    },
    {
        "chart_date": "20221230",
        "chart_movement": "1",
        "chart_position": "2",
        "chart_artist": "TAYLOR SWIFT",
        "chart_title": "MIDNIGHTS",
        "chart_peak": "1",
        "chart_weeks": "10"
    }
]
```


## To Do List

Potential enhancements for an indeterminate future update

* Add US Billboard Charts (e.g. URL https://www.billboard.com/charts/hot-100/2024-04-13/)
* XML Support

## Build environment & maintenance

* This utility was written on an Apple M1 Ultra based Mac running Sonoma 14.4.1 and Python version 3.9.6..
* Written and tested in May 2024 - note that data formats of the source may vary over time. causing the programme to fail.
* This code is unmaintained.

## Other code that has similar functionality
* https://pypi.org/project/uk-charts-api
* https://medium.com/@caineosborne/analysing-uk-chart-history-1956-to-2017-6fec0ecc991b
* https://www.markhneedham.com/blog/2020/01/04/quick-graph-uk-official-charts/