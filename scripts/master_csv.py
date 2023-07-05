import argparse
from lib.rule_dump import RuleDump
from lib.constants import *
from lib.logger import logger_wrapper
import os
from pandas import DataFrame


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='LT rules master csv',
            description='Simple script that collects info on all rules and prints them as a CSV'
        )
        self.parser.add_argument('base_path')
        self.parser.add_argument('-v', '--verbosity', default='INFO')
        self.parser.add_argument('-o', '--out-dir', default='lt-master-csv')
        self.args = self.parser.parse_args()
        os.makedirs(self.args.out_dir, exist_ok=True)


# table schema:
# id
# locale
# source repo
# type (grammar, style, unknown)
# source file
# tone_tags
# is_goal_specific
def __main__():
    cli = CLI()
    logger = logger_wrapper(cli.parser.prog, cli.args.verbosity)
    logger.debug(f"Starting script...\nInvoked with options: {cli.args}")
    out_path = path.join(cli.args.out_dir, 'all_rules.csv')
    headers = ['id', 'locale', 'source_repo', 'type', 'source_file', 'tone_tags', 'is_goal_specific']
    rows = []
    for locale in LOCALES:
        for repo_name, repo_dir in REPOS.items():
            repo_path = path.join(cli.args.base_path, repo_dir)
            dump = RuleDump(repo_path, locale)
            for file in dump.files:
                for rule in file.rules:
                    rows.append([
                        rule.id, locale, repo_name, file.type, file.rel_path,
                        ','.join([tt.tag for tt in rule.tone_tags]),
                        rule.is_goal_specific
                    ])
    df = DataFrame(rows, columns=headers)
    logger.info(df.describe())
    out_file = open(out_path, 'w')
    out_file.write(df.to_csv())


__main__()
