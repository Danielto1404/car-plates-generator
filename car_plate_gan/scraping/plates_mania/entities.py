import dataclasses
from typing import Iterable, List


def _get_field_names(obj_or_clazz: dataclasses.dataclass) -> List[str]:
    fields = dataclasses.fields(obj_or_clazz)

    return list(
        map(lambda f: f.name, fields)
    )


@dataclasses.dataclass
class CsvContentProvider:
    @classmethod
    def csv_header(cls) -> str:
        fields = _get_field_names(cls)
        fields = map(str, fields)
        return CsvContentProvider._to_csv_row(fields)

    def to_csv_row(self) -> str:
        fields = _get_field_names(self)

        values = map(lambda field: str(self.__getattribute__(field)), fields)

        return CsvContentProvider._to_csv_row(values)

    @staticmethod
    def _to_csv_row(values: Iterable[str]) -> str:
        return ",".join(values)


@dataclasses.dataclass
class ParsedItem(CsvContentProvider):
    item_id: str
    car_name: str
    car_img: str
    plate_number: str
    small_plate_img: str


__all__ = [
    "CsvContentProvider",
    "ParsedItem"
]
