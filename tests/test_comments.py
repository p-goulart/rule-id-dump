import unittest
from tests.mock import mock_rule


class TestComments(unittest.TestCase):
    def test_comment_from_rule(self):
        rule = mock_rule('<rule id="foo" tone_tags="professional formal">'
                         '<!-- MB@2023-06-23 - DESC: Removes pov from sentence for academic papers -->'
                         '<!-- MB@2023-07-03 - TODO: add more antipatterns -->'
                         '<pattern/>'
                         '</rule>')
        self.assertEquals(len(rule.comments), 2)
        comment = "<!-- MB@2023-06-23 - DESC: Removes pov from sentence for academic papers -->"
        author, date, tag, content = "MB", "2023-07-03", "TODO", "add more antipatterns "
        self.assertEquals(str(rule.comments[0].__str__()), comment)
        self.assertEquals(str(rule.comments[1].author), author)
        self.assertEquals(str(rule.comments[1].date), date)
        self.assertEquals(str(rule.comments[1].tag), tag)
        self.assertEquals(str(rule.comments[1].content), content)

    def test_ignore_comments_wrong_pos(self):
        rule = mock_rule('<rule id="foo" tone_tags="professional formal">'
                         '<!-- MB@2023-06-23 - DESC: Removes pov from sentence for academic papers -->'
                         '<antipattern>'
                         '<!-- MB@2023-07-03 - TODO: add antipatterns -->'
                         '</antipattern><pattern>'
                         '<!-- MB@2023-07-03 - TODO: add exceptions-->'
                         '</pattern>'
                         '</rule>')
        self.assertEquals(len(rule.comments), 1)


if __name__ == '__main__':
    unittest.main()
