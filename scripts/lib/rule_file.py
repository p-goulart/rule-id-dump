from os import path
from lxml import etree
from elements import Rule, RuleGroup, Category
import re


class RuleFile:
    # Used to remove entities from XML strings, as they're not needed
    entity_pattern = r"&\w+;"

    # Constructor takes as param only filepath, and derives from it a parsed XML tree
    # and a list of Rule instances.
    def __init__(self, filepath: str, rules_path: str):
        self.filepath = filepath
        self.tree = self.parse_xml()
        self.rel_path = path.relpath(self.filepath, rules_path)

    # Parse XML from path, return parsed element tree.
    def parse_xml(self):
        # No need to resolve them or load external files.
        parser = etree.XMLParser(load_dtd=False, resolve_entities=False)
        return etree.fromstring(self.xml_string, parser=parser)

    # Clean up XML string from filepath; namely, we just need to remove entities as those can't be resolved properly,
    # and they'd just slow everything down anyway.
    @property
    def xml_string(self):
        return re.sub(
            self.entity_pattern, 'REPLACED_ENTITY', open(self.filepath, encoding='utf-8').read()).encode('utf-8')

    @property
    def name(self):
        return path.basename(self.filepath)

    @property
    def categories(self):
        return [Category(node) for node in self.tree.findall('./category')]

    @property
    def rulegroups(self):
        return [RuleGroup(node) for node in self.tree.findall('./rulegroup')] + \
            [rg for rglist in [cat.rulegroups for cat in self.categories] for rg in rglist]

    # Extract rules from everything it can
    @property
    def rules(self):
        return [Rule(node) for node in self.tree.findall('./rule')] + \
            [r for rlist in [rulegroup.rules for rulegroup in self.rulegroups] for r in rlist] + \
            [r for rlist in [category.rules for category in self.categories] for r in rlist]

    @property
    def ids(self):
        id_nodes = self.tree.findall('.//rule[@id]') + self.tree.findall('.//rulegroup[@id]')
        return [node.attrib['id'] for node in id_nodes]

    @property
    def type(self):
        # lol python is goofy sometimes
        if 'grammar' in self.name:
            return 'grammar'
        if 'style' in self.name:
            return 'style'
        return 'unknown'
