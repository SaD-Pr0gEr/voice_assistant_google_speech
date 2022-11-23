import os


class FileManager:

    @staticmethod
    def get_or_create_path(path: str):
        if os.path.exists(path):
            return path
        os.makedirs(path)
        return path

    @staticmethod
    def load(file_path: str, encoding: str = "utf-8") -> str:
        with open(file_path, "r", encoding=encoding) as file:
            data = file.read()
        return data

    @staticmethod
    def raw_load(file_path: str) -> bytes:
        with open(file_path, "rb") as file:
            data = file.read()
        return data

    @staticmethod
    def write(file_path: str, content: str, encoding: str = "utf-8") -> str:
        with open(file_path, "w", encoding=encoding) as file:
            file.write(content)
        return file_path

    @staticmethod
    def raw_write(file_path: str, content: bytes) -> str:
        with open(file_path, "wb") as file:
            file.write(content)
        return file_path
