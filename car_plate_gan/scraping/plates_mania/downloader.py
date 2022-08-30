import enum
import os.path
from os import PathLike
from time import sleep
import multiprocessing as mp
from typing import Union, List

import cfscrape
import requests
from tqdm import tqdm

from car_plate_gan.scraping.csv import CsvWriter
from .entities import ParsedItem
from .parser import PlatesManiaHTMLParser


class Country(enum.Enum):
    RU = "ru"
    US = "us"


class PlatesManiaDownloader:
    def __init__(
            self,
            root: Union[str, PathLike[str]],
            country: Country = Country.RU,
            base_url: str = "https://platesmania.com"
    ):
        self.root = root
        self.scrapper = cfscrape.create_scraper()
        self.parser = PlatesManiaHTMLParser()
        self.country = country
        self.base_url = base_url

        self.images_folder = os.path.join(root, "images")
        os.makedirs(self.images_folder, exist_ok=True)

    def download(self, from_page: int = 0, to_page: int = 10):

        writer = CsvWriter(os.path.join(self.root, "data.csv"), clazz=ParsedItem)

        for page in tqdm(range(from_page, to_page), desc="Scraping page"):
            try:
                self._download_page(writer, page)
            except requests.exceptions.TooManyRedirects:
                pass

    def _download_page(self, writer: CsvWriter, page_index: int):
        items = self._extract_gallery_items(page_index)

        writer.write(items)

        for item in items:
            self._download_image(item.item_id)

    def _get_country_endpoint(self):
        return f"{self.base_url}/{self.country.value}"

    def _get_gallery_page_endpoint(self, page_index: int):
        endpoint = f"{self._get_country_endpoint()}/gallery"

        if page_index != 0:
            endpoint = f"{endpoint}-{page_index - 1}"

        return endpoint

    def _get_item_endpoint(self, item_id: str):
        return f"{self._get_country_endpoint()}/{item_id}"

    @staticmethod
    def _get_image_endpoint(item_id):
        return f"https://img03.platesmania.com/220830/o/{item_id}.jpg"

    def _extract_gallery_items(self, page_index: int) -> List[ParsedItem]:
        url = self._get_gallery_page_endpoint(page_index)
        html = self.scrapper.get(url).content
        item_ids = self.parser.extract_item_ids_from_gallery(html)

        links = [self._get_item_endpoint(item_id) for item_id in item_ids]
        htmls = [self.scrapper.get(link).content for link in links]

        return self.parser.parse_items(htmls)

    def _download_image(self, item_id: str):
        link = self._get_image_endpoint(item_id)
        data = self.scrapper.get(link).content
        path = os.path.join(self.images_folder, item_id + ".jpg")

        with open(path, 'wb') as writer:
            writer.write(data)
