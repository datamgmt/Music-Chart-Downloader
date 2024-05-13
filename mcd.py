#!/usr/bin/python3

"""
Music Chart Downloader (mcd.py) by David M Walker
(c) 2024 Data Management & Warehousing

A utility to download music charts from various sources and convert them
to csv or json formatted files
"""

import argparse
import concurrent.futures
import csv
import datetime
import json
import os
import sys
import requests
from bs4 import BeautifulSoup


def csv_writer(filename, content):
    """
    Write output to a csv file
    """

    fieldnames = ["chart_date", "chart_position", "chart_artist",
                  "chart_title", "chart_movement", "chart_peak", "chart_weeks"]

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            lineterminator=os.linesep)
        writer.writeheader()
        writer.writerows(content)


def date_validator(check_date, chart):
    """
    Validate date meets requirements for downloading chart
    """

    today = datetime.date.today()

    chart_day = chart_data[chart]["day"]
    first_chart_date = chart_data[chart]["first"]
    last_chart_date = today - \
        datetime.timedelta((7 - chart_day + today.weekday()) % 7)

    # Try to convert to a date object
    try:
        check_date = datetime.datetime.strptime(check_date, "%Y%m%d")
    except ValueError:
        sys.exit("Incorrect data format, should be YYYYMMDD")

    # Move to the last chart day
    check_date = check_date - \
        datetime.timedelta((7 - chart_day + check_date.weekday()) % 7)
    check_date = check_date.date()

    # Set minimum date to first date for chart
    check_date = max(check_date, first_chart_date)

    # Set maximum date to the most recent chart
    check_date = min(check_date, last_chart_date)

    return check_date


def download_file(url, local_filename):
    """
    Function to download the file for a given week
    """

    if not os.path.exists(local_filename):
        with requests.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)


def json_writer(filename, content):
    """
    Write output to a json file
    """

    # Serializing json
    json_object = json.dumps(content, indent=4) + "\n:"

    with open(filename, "w", newline="", encoding="utf-8") as jsonfile:
        jsonfile.write(json_object)


def process_files_for_date(working_date):
    """
    Fetch URL and then parse subsequent file
    """

    date_string = working_date.strftime("%Y%m%d")
    print(f"Processing: {args.chart}-{date_string}")

    page = f"{args.chart_url_prefix}/{date_string}"
    local_html = f"{args.datadir}/html/{args.chart}-{date_string}.html"
    download_file(page, local_html)

    with open(local_html, "r", encoding="utf-8") as file:
        file_content = process_html_file(file, working_date, args.chart)
        if "all" in args.output_set:
            all_content.extend(file_content)
        if "weekly" in args.output_set:
            if "csv" in args.output_type:
                csv_writer(
                    f"{args.datadir}/csv/{args.chart}-{date_string}.csv",
                    file_content)
            if "json" in args.output_type:
                json_writer(
                    f"{args.datadir}/json/{args.chart}-{date_string}.json",
                    file_content)


def process_html_file(filehandle, chart_date, chart):
    """
    Parse the header information of the HTML file and
    then call the function to parse each chart entry
    """

    soup = BeautifulSoup(filehandle.read(), "html.parser")

    chart_entries = []

    if chart in ("uk-singles", "uk-albums"):

        rows = list(soup.select("div.chart-item"))

        for row in rows:
            entry = process_officialcharts_entry(row, chart_date)
            if entry["chart_position"]:
                chart_entries.append(entry)

    return chart_entries


def process_officialcharts_entry(rowdata, entry_date):
    """
    Parse each entry for a UK Singles Chart format file
    """

    entry = {"chart_date": datetime.datetime.strftime(entry_date, "%Y%m%d"),
             "chart_movement": "New"}

    if len(rowdata.select("div.chart-item-content div.position strong")):
        entry["chart_position"] = rowdata.select("div.position strong")[0].text
    else:
        entry["chart_position"] = 0
        return entry

    if len(rowdata.select("a.chart-artist span")):
        entry["chart_artist"] = rowdata.select("a.chart-artist span")[0].text

    if len(rowdata.select("a.chart-name span")):
        # Specifically deal the first chart where there is no movement
        if len(rowdata.select("a.chart-name span")) == 1:
            entry["chart_title"] = rowdata.select("a.chart-name span")[0].text
        else:
            entry["chart_title"] = rowdata.select("a.chart-name span")[1].text

    if len(rowdata.select("li.movement span")):
        entry["chart_movement"] = rowdata.select("li.movement span")[1].text

    if len(rowdata.select("li.peak span")):
        entry["chart_peak"] = rowdata.select("li.peak span")[0].text

    if len(rowdata.select("li.weeks span")):
        entry["chart_weeks"] = rowdata.select("li.weeks span")[0].text

    return entry


def validate_args(arglist):
    """
    Validate all passed parameters
    """

    arglist.startdate = date_validator(arglist.startdate, arglist.chart)
    arglist.enddate = date_validator(arglist.enddate, arglist.chart)

    if arglist.startdate > arglist.enddate:
        print(
            f"Warning: Start Date ({arglist.startdate}) is after End Date ({arglist.enddate})")
        print("         Automatically transposing start and end dates")
        tmp_date = arglist.startdate
        arglist.startdate = arglist.enddate
        arglist.enddate = tmp_date

    folder_list = ["html"]
    folder_list.extend(arglist.output_type)
    for folder in folder_list:
        if not os.path.exists(f"{arglist.datadir}/{folder}"):
            try:
                os.makedirs(f"{arglist.datadir}/{folder}")
            except OSError:
                sys.exit(
                    f"Failed to make directory {arglist.datadir}/{folder}")

    arglist.chart_url_prefix = chart_data[arglist.chart]["url"]

    return arglist


# Parameter and option configuration

parser = argparse.ArgumentParser(
    description="The Music Chart Data Collector",
    epilog="(c)2024 Data Management & Warehousing ")
parser.add_argument(
    "--chart",
    choices=[
        "uk-singles",
        "uk-albums"],
    default="uk-singles",
    help="Which music chart to download, (Default: %(default)s)")
parser.add_argument(
    "--startdate",
    default="19521114",
    help="The first chart to download in YYYYMMDD format (Default: %(default)s)")
parser.add_argument(
    "--enddate",
    default=datetime.date.today().strftime("%Y%m%d"),
    help="The last chart to download in YYYYMMDD format (Default: %(default)s)")
parser.add_argument(
    "--datadir",
    default="./data",
    help="Location of datafiles used in processing (Default: %(default)s)")
parser.add_argument("--output_type",
                    nargs="*",
                    choices=["csv", "json"],
                    default=["csv"],
                    help="Output file formats required (Default: %(default)s)")
parser.add_argument(
    "--output_set",
    nargs="*",
    choices=[
        "weekly",
        "all"],
    default=["all"],
    help="Weekly charts and/or one large file (Default: %(default)s)")

# url: URL of the historical charts
# day: Day of week chart released (0=Monday ... 6=Sunday)
# first: Dates of the very first chart for each organisation
chart_data = {"uk-singles": {"url": "https://www.officialcharts.com/charts/singles-chart/",
                             "day": 4,
                             "first": datetime.date(1952, 11, 14)},
              "uk-albums": {"url": "https://www.officialcharts.com/charts/albums-chart/",
                            "day": 4,
                            "first": datetime.date(1956, 7, 28)},
              "billboard-top-100": {"url": "undefined",
                                    "day": 6,
                                    "first": datetime.date(1958, 8, 4)}
              }

args = validate_args(parser.parse_args())

fetchdate = args.startdate
all_content = []

pool = concurrent.futures.ThreadPoolExecutor()

while fetchdate <= args.enddate:

    pool.submit(process_files_for_date(fetchdate))
    fetchdate = fetchdate + datetime.timedelta(7)

pool.shutdown(wait=True)


if "all" in args.output_set:
    if "csv" in args.output_type:
        csv_writer(f"{args.datadir}/csv/{args.chart}-all.csv", all_content)
    if "json" in args.output_type:
        json_writer(f"{args.datadir}/json/{args.chart}-all.json", all_content)

print("Finished")
