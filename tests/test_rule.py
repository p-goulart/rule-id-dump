from scripts.lib.elements import Rule, RuleGroup, Category
import xml.etree.ElementTree as XMLTree
import unittest


class TestRule(unittest.TestCase):
    @staticmethod
    def mock_rule(xml_str: str, parent_attrib=None):
        return Rule(XMLTree.fromstring(xml_str), parent_attrib)

    def test_rule_constructor(self):
        self.assertIsInstance(self.mock_rule('<rule id="foo" name="bar"/>'), Rule)

    def test_rule_id(self):
        self.assertEqual(self.mock_rule('<rule id="foo" name="bar"/>').id, 'foo')

    def test_rule_id_parent_id(self):
        rule = self.mock_rule('<rule name="bar"/>', {'id': 'parent_id'})
        self.assertEquals(rule.id, 'parent_id')

    def test_rule_from_rulegroup(self):
        xml_str = '<rulegroup id="foo"><rule name="bar"/><rule id="pub"/></rulegroup>'
        rulegroup = RuleGroup(XMLTree.fromstring(xml_str), {'xyz': 'abc'})
        rules = rulegroup.rules
        self.assertEquals(len(rules), 2)
        self.assertEquals(rules[0].id, 'foo')
        self.assertEquals(rules[1].id, 'pub')
        self.assertEquals(rules[0].attrib['xyz'], 'abc')


if __name__ == '__main__':
    unittest.main()
