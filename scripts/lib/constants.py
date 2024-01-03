from os import path
import re

RULES_PATH = path.join('src', 'main', 'resources', 'org', 'languagetool', 'rules')
LOCALES = {'de', 'es', 'en', 'fr', 'nl', 'pt'}
REPOS = {'os': 'languagetool',
         'premium': 'languagetool-premium-modules'}

WRITING_GOAL_MAPPING = {
    "serious": ['clarity', 'confident', 'formal', 'general', 'positive', 'professional'],
    "objective": ['academic', 'clarity', 'formal', 'general', 'objective', 'povrem', 'scientific'],
    "confident": ['clarity', 'confident', 'general', 'persuasive', 'positive'],
    "personal": ['clarity', 'general', 'informal', 'positive', 'povadd'],
    "expressive": ['clarity', 'general']
}

COMMENT_REGEX = re.compile(r'<!-- (?P<author>[\w-]+)@(?P<date>\d{4}-\d{2}-\d{2}) - (?P<tag>[A-Z]+): '
                           r'(?P<content>[\s\S\n]*?)-->')
