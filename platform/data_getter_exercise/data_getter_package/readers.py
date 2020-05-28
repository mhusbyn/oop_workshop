import abc
from typing import Iterable, Dict

from platform.data_getter_exercise.data_getter_package.connections import IDataSource


class IDataReader(abc.ABC):
    @abc.abstractmethod
    def get_data(self) -> Iterable[Dict[str, str]]:
        pass


class CSVDataReader(IDataReader):
    def __init__(self, data_connection: IDataSource):
        self._data_connection = data_connection

    def get_data(self) -> Iterable[Dict[str, str]]:
        with self._data_connection.read_data() as file:
            # Go line by line, parse and yield dict
            for line in file:
                yield self._parse_line(line)

    def _parse_line(self, line: str) -> Dict[str, str]:
        pass


class JsonDataReader(IDataReader):
    def __init__(self, data_connection: IDataSource):
        self._data_connection = data_connection

    def get_data(self) -> Iterable[Dict[str, str]]:
        with self._data_connection.read_data() as file:
            return self._parse_file(file)

    def _parse_file(self, file: bytes) -> Iterable[Dict[str, str]]:
        pass
