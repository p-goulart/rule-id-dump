from glob import glob
from constants import *
from rule_file import RuleFile


class RuleDump:
    # Construct with path to repository (because OS & premium are kept separate) and locale.
    def __init__(self, repo_path: str, locale: str):
        self.repo_path = repo_path
        self.locale = locale

    # Globs repo for rule/style XMLs and, for each file found, constructs a RuleFile object
    @property
    def files(self):
        glob_dir = path.join(self.repo_path, 'languagetool-language-modules',
                             f"{self.locale}*", RULES_PATH, self.locale,
                             '**', '*.xml')
        return [RuleFile(p) for p in glob(glob_dir, recursive=True)]

    # Return flattened, uniqed, sorted list of IDs from all files
    @property
    def ids(self):
        return sorted(list(set([i for id_list in [f.ids for f in self.files] for i in id_list])))
