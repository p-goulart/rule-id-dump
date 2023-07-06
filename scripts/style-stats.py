import argparse
import os
from lib.logger import logger_wrapper
from lib.rule_dump import RuleDump
from lib.constants import *
from pandas import DataFrame
import collections


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='LT style stats',
            description='Simple script that compiles stats on style rule creation'
        )
        self.parser.add_argument('-v', '--verbosity', default='INFO')
        self.parser.add_argument('-o', '--out-dir', default='lt-style-out')
        self.parser.add_argument('-f', '--from-dir')
        self.parser.add_argument('-t', '--to-dir')
        self.args = self.parser.parse_args()
        os.makedirs(self.args.out_dir, exist_ok=True)


def rows_from_rule(rule, repo_name, row_list):
    # create a separate entry for each tone_tag 🥴
    tone_tags = rule.tone_tags
    if len(tone_tags) == 0:
        row_list.append([
            rule.id,
            'untagged',
            repo_name
        ])
    for tt in rule.tone_tags:
        row_list.append([
            rule.id,
            tt.tag,
            repo_name
        ])


def df_from_repo(to_dir, repo_dir, repo_name, locale, row_list):
    repo_path = os.path.join(to_dir, repo_dir)
    dump = RuleDump(repo_path, locale, 'style')
    for rule in [rule for rule_list in [file.rules for file in dump.files] for rule in rule_list]:
        rows_from_rule(rule, repo_name, row_list)


# Also prints, because lazy
def compare_dfs(df_to, df_from):
    coll_to = collections.Counter(df_to['tone_tags'])
    coll_from = collections.Counter(df_from['tone_tags'])
    coll_to.subtract(coll_from)
    return "\n".join([f"{key},{value}" for key, value in coll_to.items()])


def __main__():
    cli = CLI()
    logger = logger_wrapper(cli.parser.prog, cli.args.verbosity)
    logger.debug(f"Starting script...\nInvoked with options: {cli.args}")
    headers = ['id', 'tone_tags', 'repo']
    for locale in LOCALES:
        locale_dir = os.path.join(cli.args.out_dir, locale)
        os.makedirs(locale_dir, exist_ok=True)
        summary_filepath = os.path.join(locale_dir, 'all_time_summary.txt')
        added_filepath = os.path.join(locale_dir, 'added_this_quarter.txt')
        logger.debug(f"Compiling style stats for {locale}...")
        rows_to = []
        rows_from = []
        for repo_name, repo_dir in REPOS.items():
            df_from_repo(cli.args.to_dir, repo_dir, repo_name, locale, rows_to)
            df_from_repo(cli.args.from_dir, repo_dir, repo_name, locale, rows_from)
        df_to = DataFrame(rows_to, columns=headers)
        df_from = DataFrame(rows_from, columns=headers)
        open(summary_filepath, 'w').write(df_to.groupby(by='repo')['tone_tags'].value_counts().to_string())
        open(added_filepath, 'w').write(compare_dfs(df_to, df_from))


__main__()
