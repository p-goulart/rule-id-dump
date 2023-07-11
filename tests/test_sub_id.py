import unittest
from tests.mock import mock_rule, mock_rulegroup


class TestSubId(unittest.TestCase):
    def test_sub_id_rule_standalone(self):
        rule = mock_rule('<rule id="foo" name="bar"/>')
        self.assertEqual(rule.sub_id, "1")

    def test_sub_id_rulegroup(self):
        rulegroup = mock_rulegroup('<rulegroup id="foo" name="foo foo"> \
        <rule id="bar" name="bar bar"/><rule/></rulegroup>')
        for index, rule in enumerate(rulegroup.rules, start=1):
            self.assertEqual(rule.sub_id, str(index))

    def test_sub_id_rulegroup_with_url(self):
        rulegroup = mock_rulegroup('<rulegroup id="foo" name="foo foo"> \
        <url/><rule id="bar" name="bar bar"/><rule/></rulegroup>')
        for index, rule in enumerate(rulegroup.rules, start=1):
            self.assertEqual(rule.sub_id, str(index))


if __name__ == '__main__':
    unittest.main()
