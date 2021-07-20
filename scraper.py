from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen

site = None
dates=[] #Date
swe=[] #SWE corresponding to that Date

url = "https://wcc.sc.egov.usda.gov/reportGenerator/view_csv/customSingleStationReport/daily/345:CO:SNTL%7Cid=%22%22%7Cname/POR_BEGIN,POR_END/WTEQ::value"
page = urlopen(url)
page = page.read().decode("utf-8")
print(page.split())