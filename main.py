import os.path

import pandas as pd

from car_plate_gan.scraping.plates_mania import PlatesManiaDownloader

if os.path.exists("resources/data.csv"):
    downloaded = set(pd.read_csv('resources/data.csv')["plate_number"].tolist())
else:
    downloaded = None

downloader = PlatesManiaDownloader("resources", downloaded=downloaded)

downloader.download(from_page=0, to_page=100, create_file=False)
