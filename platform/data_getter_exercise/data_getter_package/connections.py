import abc
from typing import Dict


class IDataSource(abc.ABC):
    @abc.abstractmethod
    def read_data(self) -> bytes:
        pass


class IFileSource(IDataSource):
    def read_data(self) -> bytes:
        return self.open(file_path=self.file_path)

    @abc.abstractmethod
    def open(self, file_path: str) -> bytes:
        pass

    @abc.abstractmethod
    @property
    def file_path(self):
        pass


class FtpFileSource(IFileSource):
    def __init__(self, connection_params: Dict, file_path: str):
        self._connection_params = connection_params
        self._file_path = file_path

    def open(self, file_path: str) -> bytes:
        # Connect to ftp server and get file
        pass

    @property
    def file_path(self):
        return self._file_path


class HttpFileSource(IFileSource):
    def __init__(self, connection_params: Dict):
        self._connection_params = connection_params

    def open(self, file_path: str) -> bytes:
        # Connect to http endpoint and get file
        pass

    @property
    def file_path(self):
        return self._connection_params['file_path']


class LocalFileSource(IFileSource):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def open(self, file_path: str) -> bytes:
        # Open file locally
        pass

    @property
    def file_path(self):
        return self._file_path


class HttpDataSource(IDataSource):
    def __init__(self, endpoint: str):
        self._endpoint = endpoint

    def read_data(self) -> bytes:
        # Send request to endpoint
        # Return request body

        return bytes()
