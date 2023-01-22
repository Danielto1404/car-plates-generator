import os
from typing import Type, Iterable

from .plates_mania.entities import CsvContentProvider

__NEWLINE__ = '\n'


class CsvWriter:
    def __init__(
            self,
            path: str,
            clazz: Type[CsvContentProvider],
            create_file: bool = True
    ):
        self.path = path
        self.clazz = clazz
        self.is_file_created = os.path.exists(path=path) and not create_file

    def write(self, iterable: Iterable):

        mode = "a" if self.is_file_created else "w"

        with open(self.path, mode=mode) as writer:
            if not self.is_file_created:
                writer.write(self.clazz.csv_header() + __NEWLINE__)
                self.is_file_created = True

            for data in iterable:
                line = data.to_csv_row()
                writer.write(line + __NEWLINE__)


__all__ = [
    "CsvWriter"
]
