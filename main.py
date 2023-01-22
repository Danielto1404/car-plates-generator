import os.path

import pandas as pd

from car_plate_gan.scraping.plates_mania import PlatesManiaDownloader

if os.path.exists("dataset/data.csv"):
    downloaded = set(pd.read_csv('dataset/data.csv')["plate_number"].tolist())
else:
    downloaded = None

downloader = PlatesManiaDownloader("dataset", downloaded=downloaded)

downloader.download(from_page=100, to_page=200, create_file=False)
