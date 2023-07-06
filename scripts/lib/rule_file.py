from os import path
from lxml import etree
from elements import Rule, RuleGroup, Category


class RuleFile:
    # Constructor takes as param only filepath, and derives from it a parsed XML tree
    # and a list of Rule instances.
    def __init__(self, filepath: str, rules_path: str):
        self.filepath = filepath
        self.tree = self.parse_xml()
        self.rel_path = path.relpath(self.filepath, rules_path)

    # Parse XML from path, return parsed element tree.
    def parse_xml(self):
        return etree.parse(self.filepath)

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
