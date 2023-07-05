import xml.etree.ElementTree as XMLTree
from typing import List


class ToneTag:
    def __init__(self, tag_str):
        self.tag = tag_str

    def __str__(self):
        return f"ToneTag<{self.tag}>"

    @staticmethod
    def list_from_str(tag_str_list) -> List:
        return [ToneTag(tag) for tag in tag_str_list.split(' ')]


class Element:
    # Construct instance with XML node only.
    def __init__(self, xml_node: XMLTree, parent_attrib=None):
        if parent_attrib is None:
            parent_attrib = {}
        self.xml_node = xml_node
        # messy, overwrites tone_tags
        self.attrib = {**parent_attrib, **self.xml_node.attrib}
        self.parent_attrib = parent_attrib
        self.tone_tags = self.combine_tone_tags(self.xml_node.attrib, parent_attrib)

    @property
    def rulegroups(self):
        return [RuleGroup(node, self.attrib) for node in self.xml_node.findall('./rulegroup')]

    @property
    def rules(self):
        return [Rule(node, self.attrib) for node in self.xml_node.findall('./rule')]

    # Will return parent's ID if None
    @property
    def id(self):
        try:
            return self.attrib['id']
        except KeyError:
            return None

    # This is stupid, but whatever, it works.
    @staticmethod
    def combine_tone_tags(attrib, parent_attrib) -> List[ToneTag]:
        try:
            child_tt = ToneTag.list_from_str(attrib['tone_tags'])
        except KeyError:
            child_tt: List[ToneTag] = []
        try:
            parent_tt = ToneTag.list_from_str(parent_attrib['tone_tags'])
        except KeyError:
            parent_tt: List[ToneTag] = []
        return child_tt + parent_tt


class Category(Element):
    def __init__(self, xml_node: XMLTree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)


class RuleGroup(Element):
    def __init__(self, xml_node: XMLTree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)


class Rule(Element):
    def __init__(self, xml_node: XMLTree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)
