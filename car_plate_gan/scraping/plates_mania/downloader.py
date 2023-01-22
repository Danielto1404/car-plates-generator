import enum
import os.path
from os import PathLike
from typing import Union, List, Optional, Set

import cfscrape
import requests
import tqdm
from tqdm import trange

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
            base_url: str = "https://platesmania.com",
            downloaded: Optional[Set[str]] = None
    ):
        self.root = root
        self.scrapper = cfscrape.create_scraper()
        self.parser = PlatesManiaHTMLParser()
        self.country = country
        self.base_url = base_url

        if downloaded is None:
            self.downloaded = set()
        else:
            self.downloaded = downloaded

        self.images_folder = os.path.join(root, "images")

        os.makedirs(self.images_folder, exist_ok=True)

    def download(
            self,
            from_page: int = 0,
            to_page: int = 10,
            create_file: bool = True
    ):

        writer = CsvWriter(os.path.join(self.root, "data.csv"), clazz=ParsedItem, create_file=create_file)
        progress = trange(from_page, to_page, desc="scraping page")

        for page in progress:
            try:
                self._download_page(writer, page, progress)
            except requests.exceptions.TooManyRedirects as e:
                print(e)

    def _download_page(self, writer: CsvWriter, page_index: int, progress: tqdm.tqdm):
        items = self._extract_gallery_items(page_index)
        items = [i for i in items if i is not None]

        unique_ids = set()
        unique_items = []

        for item in items:
            if item.plate_number not in unique_ids:
                unique_items.append(item)
                unique_ids.add(item.plate_number)

        items = [item for item in items if item.plate_number not in self.downloaded]
        self.downloaded |= set([item.plate_number for item in items])

        writer.write(items)

        for item in items:
            self._download_image(item.item_id)

        progress.set_postfix_str(f"downloaded: {len(items)}")

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

    def _extract_gallery_items(self, page_index: int) -> List[Optional[ParsedItem]]:
        url = self._get_gallery_page_endpoint(page_index)
        html = self.scrapper.get(url).content
        item_ids = self.parser.extract_item_ids_from_gallery(html)

        links = [self._get_item_endpoint(item_id) for item_id in item_ids]
        htmls = [self.scrapper.get(link).content for link in links]

        return self.parser.parse_items(htmls)

    def _download_image(self, item_id: str):
        path = os.path.join(self.images_folder, item_id + ".jpg")
        link = self._get_image_endpoint(item_id)
        data = self.scrapper.get(link).content

        with open(path, 'wb') as writer:
            writer.write(data)


__all__ = [
    "Country",
    "PlatesManiaDownloader"
]
