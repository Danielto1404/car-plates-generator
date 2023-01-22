from typing import List, Optional

import bs4
from bs4 import BeautifulSoup

from .entities import ParsedItem


class PlatesManiaHTMLParser:
    @staticmethod
    def extract_item_ids_from_gallery(html) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")

        items = soup.find_all("div", class_="panel-body")

        # /us/nomer19826107
        hrefs = [item.find("a").get("href") for item in items]

        # nomer19826107
        hrefs = [href.split("/")[-1] for href in hrefs]

        return hrefs

    @staticmethod
    def parse_items(htmls: List[bytes]) -> List[Optional[ParsedItem]]:
        return [PlatesManiaHTMLParser.parse_item(html) for html in htmls]

    @staticmethod
    def extract_car_name(content: bs4.Tag) -> str:
        hrefs = content \
            .find("h3", class_="text-center margin-bottom-10") \
            .find_all("a")

        name_parts = [href.text for href in hrefs]
        car_name = " ".join(name_parts).replace(",", " ")

        return car_name

    @staticmethod
    def extract_small_plate_image_link(content: bs4.Tag) -> str:
        return content \
            .find("img", class_="img-responsive center-block margin-bottom-20") \
            .get("src")

    @staticmethod
    def extract_car_tag(content: bs4.Tag) -> bs4.Tag:
        return content.find("img", class_="img-responsive center-block")

    @staticmethod
    def extract_plate_number(car_tag: bs4.Tag) -> str:
        x = car_tag.get("alt").split(",")[0]
        return "".join(x.split()).upper()

    @staticmethod
    def extract_car_image_link(car_tag: bs4.Tag) -> str:
        return car_tag.get("src")

    @staticmethod
    def extract_car_id(car_img: str):
        return car_img.split("/")[-1].split(".")[0]

    @staticmethod
    def parse_item(html) -> Optional[ParsedItem]:
        soup = BeautifulSoup(html, "html.parser")

        content = soup.find("div", class_="container content")

        if content is not None:
            content = content.find("div", class_="panel-body")

        if content is None:
            return None

        car_name = PlatesManiaHTMLParser.extract_car_name(content)
        small_plate_img = PlatesManiaHTMLParser.extract_small_plate_image_link(content)
        car_tag = PlatesManiaHTMLParser.extract_car_tag(content)
        plate_number = PlatesManiaHTMLParser.extract_plate_number(car_tag)
        car_img = PlatesManiaHTMLParser.extract_car_image_link(car_tag)
        item_id = PlatesManiaHTMLParser.extract_car_id(car_img)

        return ParsedItem(
            car_name=car_name,
            car_img=car_img,
            plate_number=plate_number,
            small_plate_img=small_plate_img,
            item_id=item_id
        )


__all__ = [
    "PlatesManiaHTMLParser"
]
