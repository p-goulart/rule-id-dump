import unittest
from tests.mock import mock_rule
from scripts.lib.elements import ToneTag


class TestToneTags(unittest.TestCase):
    def test_tone_tags(self):
        tone_tag_list = ToneTag.list_from_str('a b c')
        self.assertEqual(len(tone_tag_list), 3)
        self.assertEquals(tone_tag_list[1].tag, 'b')
        self.assertIsInstance(tone_tag_list[0], ToneTag)

    def test_tone_tag_from_rule(self):
        rule = mock_rule('<rule id="foo" tone_tags="professional formal"/>')
        self.assertEquals(len(rule.tone_tags), 2)
        self.assertEquals(rule.tone_tags[0].tag, 'professional')

    def test_tone_tag_inheritance(self):
        rule = mock_rule('<rule id="foo" tone_tags="professional formal"/>',
                         {'tone_tags': 'academic potato'})
        self.assertEquals(len(rule.tone_tags), 4)


if __name__ == '__main__':
    unittest.main()
