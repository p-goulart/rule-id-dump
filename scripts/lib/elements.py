import re
from lxml import etree
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
    def __init__(self, xml_node: etree, parent_attrib=None):
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

    @property
    def sub_id(self):
        if self.xml_node.tag == "rule":
            if self.xml_node.getparent() is not None and self.xml_node.getparent().tag == "rulegroup":
                return str(len(self.xml_node.xpath("preceding-sibling::rule")) + 1)
            else:
                return "1"

    @property
    def is_goal_specific(self):
        try:
            return self.attrib['is_goal_specific']
        except KeyError:
            return 'false'

    @property
    def comments(self):
        if self.xml_node.tag in ["rule", "rulegroup"]:
            regex = re.compile(r'<!-- [A-Z]{2}@\d{4}-\d{2}-\d{2} - [A-Z]+: [\w|\s]+-->')
            comments = self.xml_node.xpath("./comment()[not(preceding-sibling::pattern)]")
            return [Comment(c) for c in comments if re.fullmatch(regex, str(c))]

    # This is stupid, but whatever, it works.
    @staticmethod
    def combine_tone_tags(attrib, parent_attrib) -> List[ToneTag]:
        tt = []
        try:
            tt = tt + attrib['tone_tags'].split(' ')
        except KeyError:
            pass
        try:
            tt = tt + parent_attrib['tone_tags'].split(' ')
        except KeyError:
            pass
        return [ToneTag(t) for t in list(set(tt))]


class Category(Element):
    def __init__(self, xml_node: etree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)


class RuleGroup(Element):
    def __init__(self, xml_node: etree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)


class Rule(Element):
    def __init__(self, xml_node: etree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)


class Comment:
    def __init__(self, comment_str):
        self.comment = comment_str

    def __str__(self):
        return self.comment

    @property
    def author(self):
        return re.search(r'<!-- ([A-Z]{2}).*', self.comment.__str__()).group(1)

    @property
    def date(self):
        return re.search(r'<!-- [A-Z]{2}@(\d{4}-\d{2}-\d{2}) - [A-Z]+: [\w|\s]+-->', self.comment.__str__()).group(1)

    @property
    def tag(self):
        return re.search(r'<!-- [A-Z]{2}@\d{4}-\d{2}-\d{2} - ([A-Z]+): [\w|\s]+-->', self.comment.__str__()).group(1)

    @property
    def content(self):
        return re.search(r'<!-- [A-Z]{2}@\d{4}-\d{2}-\d{2} - [A-Z]+: ([\w|\s]+)-->', self.comment.__str__()).group(1)
