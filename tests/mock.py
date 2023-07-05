from os import path
import pathlib


def mock_path(*parts):
    return path.join(pathlib.Path(__file__).parent.resolve(), 'mock', *parts)
