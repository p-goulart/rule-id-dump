from os import path
import pathlib
from scripts.lib.elements import Rule
import xml.etree.ElementTree as XMLTree


def mock_path(*parts):
    return path.join(pathlib.Path(__file__).parent.resolve(), 'mock', *parts)


def mock_rule(xml_str: str, parent_attrib=None):
    return Rule(XMLTree.fromstring(xml_str), parent_attrib)
