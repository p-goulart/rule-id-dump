from scripts.lib.elements import Rule, RuleGroup
from lxml import etree
import unittest
from tests.mock import mock_rule


class TestRule(unittest.TestCase):
    def test_rule_constructor(self):
        self.assertIsInstance(mock_rule('<rule id="foo" name="bar"/>'), Rule)

    def test_rule_id(self):
        self.assertEqual(mock_rule('<rule id="foo" name="bar"/>').id, 'foo')

    def test_rule_id_parent_id(self):
        rule = mock_rule('<rule name="bar"/>', {'id': 'parent_id'})
        self.assertEquals(rule.id, 'parent_id')

    def test_rule_from_rulegroup(self):
        xml_str = '<rulegroup id="foo"><rule name="bar"/><rule id="pub"/></rulegroup>'
        rulegroup = RuleGroup(etree.fromstring(xml_str), {'xyz': 'abc'})
        rules = rulegroup.rules
        self.assertEquals(len(rules), 2)
        self.assertEquals(rules[0].id, 'foo')
        self.assertEquals(rules[1].id, 'pub')
        self.assertEquals(rules[0].attrib['xyz'], 'abc')


if __name__ == '__main__':
    unittest.main()
