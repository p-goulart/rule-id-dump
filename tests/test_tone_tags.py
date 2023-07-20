import unittest
from tests.mock import mock_rule
from scripts.lib.elements import ToneTag
from scripts.lib.writing_goals import WritingGoal


class TestToneTags(unittest.TestCase):
    def test_tone_tags(self):
        tone_tag_list = ToneTag.list_from_str('a b c')
        self.assertEqual(len(tone_tag_list), 3)
        self.assertEquals(tone_tag_list[1].tag, 'b')
        self.assertIsInstance(tone_tag_list[0], ToneTag)

    def test_tone_tag_from_rule(self):
        rule = mock_rule('<rule id="foo" tone_tags="professional formal"/>')
        self.assertEquals(len(rule.tone_tags), 2)
        self.assertEquals(set([t.tag for t in rule.tone_tags]),
                          {'professional', 'formal'})

    def test_tone_tag_inheritance(self):
        rule = mock_rule('<rule id="foo" tone_tags="professional formal"/>',
                         {'tone_tags': 'academic potato'})
        self.assertEquals(len(rule.tone_tags), 4)

    def test_tone_tag_inheritance_repeated(self):
        rule = mock_rule('<rule id="foo" tone_tags="formal"/>',
                         {'tone_tags': 'formal'})
        self.assertEquals(len(rule.tone_tags), 1)

    def test_writing_goal(self):
        self.assertEquals(len(WritingGoal.list_from_tags([ToneTag('clarity')])), 5)
        self.assertEquals(len(WritingGoal.list_from_tags([ToneTag('formal'), ToneTag('informal')])), 3)


if __name__ == '__main__':
    unittest.main()
