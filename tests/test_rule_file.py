import unittest
from tests.mock import mock_path
from scripts.lib.rule_file import RuleFile, Rule


class TestRuleFile(unittest.TestCase):
    good_xml_path = mock_path('loose_xml', 'good.xml')
    loose_xml_path = mock_path('loose_xml')

    def test_rule_file_constructor(self):
        rule_file = RuleFile(self.good_xml_path, self.loose_xml_path)
        self.assertIsInstance(rule_file, RuleFile)

    def test_rule_file_rules(self):
        rule_file = RuleFile(self.good_xml_path, self.loose_xml_path)
        rules = rule_file.rules
        self.assertEquals(len(rules), 3)
        self.assertIsInstance(rules[0], Rule)

    def test_rule_file_categories(self):
        rule_file = RuleFile(self.good_xml_path, self.loose_xml_path)
        cats = rule_file.categories
        self.assertEquals(len(cats), 1)
        self.assertEquals(len(cats[0].rulegroups), 0)
        self.assertEquals(len(cats[0].rules), 3)

    def test_rule_file_ids(self):
        rule_file = RuleFile(self.good_xml_path, self.loose_xml_path)
        ids = rule_file.ids
        self.assertEqual(len(ids), 3)
        self.assertEqual(ids[0], 'PARONYM_PREMIO_252_PT')

    def test_rule_file_with_groups(self):
        rule_file = RuleFile(mock_path('loose_xml', 'good_groups.xml'),
                             self.loose_xml_path)
        self.assertEquals(len(rule_file.rules), 3)
        self.assertEquals(len(rule_file.ids), 1)


if __name__ == '__main__':
    unittest.main()
