from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

URL = 'http://salah.dk'
page = requests.get(URL)
