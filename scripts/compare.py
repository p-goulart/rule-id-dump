import argparse
import os
from lib.logger import logger_wrapper
from lib.rule_dump import RuleDump
from lib.comparison import Comparison
from lib.constants import *


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='LT repo comparison',
            description='Simple script compares the states of two repos and returns a summary of added rules'
        )
        self.parser.add_argument('-v', '--verbosity', default='INFO')
        self.parser.add_argument('-o', '--out-dir', default='lt-comparison-out')
        self.parser.add_argument('-f', '--from-dir')
        self.parser.add_argument('-t', '--to-dir')
        self.args = self.parser.parse_args()
        os.makedirs(self.args.out_dir, exist_ok=True)


def __main__():
    cli = CLI()
    logger = logger_wrapper(cli.parser.prog, cli.args.verbosity)
    logger.debug(f"Starting script...\nInvoked with options: {cli.args}")
    for locale in LOCALES:
        out_dir = path.join(cli.args.out_dir, locale)
        os.makedirs(out_dir, exist_ok=True)
        for repo_name, repo_dir in REPOS.items():
            out_filename = f"{repo_name}.txt"
            out_path = path.join(out_dir, out_filename)
            from_repo_path = path.join(cli.args.from_dir, repo_dir)
            to_repo_path = path.join(cli.args.to_dir, repo_dir)
            comparison = Comparison(
                RuleDump(from_repo_path, locale),
                RuleDump(to_repo_path, locale, 'style'),
            )
            out_file = open(out_path, 'w')
            out_file.write("\n".join(comparison.added()))


__main__()
