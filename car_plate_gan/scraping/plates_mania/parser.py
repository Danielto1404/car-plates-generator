from typing import List

from bs4 import BeautifulSoup

from .entities import ParsedItem


class PlatesManiaHTMLParser:
    @staticmethod
    def extract_item_ids_from_gallery(html):
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all("div", class_="panel-body")

        # /us/nomer19826107
        hrefs = [item.find("a").get("href") for item in items]

        # nomer19826107
        hrefs = [href.split("/")[-1] for href in hrefs]

        return hrefs

    @staticmethod
    def parse_items(htmls) -> List[ParsedItem]:
        return [PlatesManiaHTMLParser.parse_item(html) for html in htmls]

    @staticmethod
    def parse_item(html) -> ParsedItem:
        soup = BeautifulSoup(html, "html.parser")

        content = soup.find("div", class_="container content").find("div", class_="panel-body")

        hrefs = content \
            .find("h3", class_="text-center margin-bottom-10") \
            .find_all("a")

        car_names = [href.text for href in hrefs]
        car_name = " ".join(car_names)

        small_plate_img = content \
            .find("img", class_="img-responsive center-block margin-bottom-20") \
            .get("src")

        car_tag = content.find("img", class_="img-responsive center-block")

        plate_number = car_tag.get("alt").split(',')[0]
        car_img = car_tag.get("src")

        return ParsedItem(
            car_name=car_name,
            car_img=car_img,
            plate_number=plate_number,
            small_plate_img=small_plate_img,
            item_id=car_img.split("/")[-1].split(".")[0]
        )
