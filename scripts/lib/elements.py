import xml.etree.ElementTree as XMLTree


class Element:
    # Construct instance with XML node only.
    def __init__(self, xml_node: XMLTree, parent_attrib=None):
        if parent_attrib is None:
            parent_attrib = {}
        self.xml_node = xml_node
        self.attrib = {**parent_attrib, **self.xml_node.attrib}
        self.parent_attrib = parent_attrib

    @property
    def rulegroups(self):
        return [RuleGroup(node, self.attrib) for node in self.xml_node.findall('./rulegroup')]

    @property
    def rules(self):
        return [Rule(node, self.attrib) for node in self.xml_node.findall('./rule')]


class Category(Element):
    def __init__(self, xml_node: XMLTree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)


class RuleGroup(Element):
    def __init__(self, xml_node: XMLTree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)


class Rule(Element):
    def __init__(self, xml_node: XMLTree, parent_attrib=None):
        super().__init__(xml_node, parent_attrib)

    # Will return parent's ID if None
    @property
    def id(self):
        try:
            return self.attrib['id']
        except KeyError:
            return None
