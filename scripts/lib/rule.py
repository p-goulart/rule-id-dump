import xml.etree.ElementTree as XMLTree


# For now, Rule objects refer to both rule *and* rulegroup nodes.
# Depending on what we need to do later, we *may* need to distinguish them.
# In which case I think RuleGroup should prob. just inherit from Rule.
class Rule:
    # Construct instance with XML node only.
    def __init__(self, xml_node: XMLTree):
        self.xml_node = xml_node
        self.attrib = self.xml_node.attrib

    @property
    def id(self):
        return self.attrib['id']
