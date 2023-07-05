from glob import glob
from constants import *
from rule_file import RuleFile


class RuleDump:
    # Construct with path to repository (because OS & premium are kept separate) and locale.
    def __init__(self, repo_path: str, locale: str, type_filter=''):
        self.repo_path = repo_path
        self.locale = locale
        self.type_filter = type_filter
        self.rules_path = self.glob_rules_path()

    def glob_rules_path(self):
        glob_dir = path.join(self.repo_path, 'languagetool-language-modules',
                             f"{self.locale}*", RULES_PATH, self.locale)
        return glob(glob_dir)[0]

    # Globs repo for rule/style XMLs and, for each file found, constructs a RuleFile object
    @property
    def files(self):
        glob_dir = path.join(self.rules_path, '**', f'{self.type_filter}*.xml')
        return [RuleFile(p, self.rules_path) for p in glob(glob_dir, recursive=True)]

    # Return flattened, uniqed, sorted list of IDs from all files
    @property
    def ids(self):
        return sorted(list(set([i for id_list in [f.ids for f in self.files] for i in id_list])))
