import xml.etree.ElementTree as XMLTree
from os import path
from rule import Rule


class RuleFile:
    # Constructor takes as param only filepath, and derives from it a parsed XML tree
    # and a list of Rule instances.
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.tree = self.parse_xml()

    # Parse XML from path, return parsed element tree.
    def parse_xml(self):
        return XMLTree.parse(self.filepath)

    @property
    def name(self):
        return path.basename(self.filepath)

    @property
    def rules(self):
        return [Rule(node) for node in self.tree.findall('.//rule[@id]') + self.tree.findall('.//rulegroup[@id]')]

    @property
    def ids(self):
        return [r.id for r in self.rules]
