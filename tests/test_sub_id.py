import unittest
from tests.mock import mock_rule


class TestSubId(unittest.TestCase):
    def test_sub_id_standalone_rule(self):
        rule = mock_rule('<rule id="foo" name="bar"/>')
        self.assertEqual(rule.sub_id, "1")


if __name__ == '__main__':
    unittest.main()
