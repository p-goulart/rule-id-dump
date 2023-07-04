import argparse
from lib.rule_dump import RuleDump
from lib.constants import *
from lib.logger import logger_wrapper
import os


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='LT rule dump',
            description='Simple script that dumps all rule IDs, from both an OS and a premium repo, for all locales'
        )
        self.parser.add_argument('base_path')
        self.parser.add_argument('-v', '--verbosity', default='INFO')
        self.parser.add_argument('-o', '--out-dir', default='lt-rule-dump-out')
        self.args = self.parser.parse_args()
        os.makedirs(self.args.out_dir, exist_ok=True)


def __main__():
    cli = CLI()
    logger = logger_wrapper('lt-rule-id-dump', cli.args.verbosity)
    logger.debug(f"Starting script...\nInvoked with options: {cli.args}")
    for repo_name, repo_dir in REPOS.items():
        for locale in LOCALES:
            out_filename = f"{repo_name}_{locale}.txt"
            repo_path = path.join(cli.args.base_path, repo_dir)
            out_path = path.join(cli.args.out_dir, out_filename)
            logger.debug(f"Printing rule IDs for {out_filename}")
            dump = RuleDump(repo_path, locale)
            out_file = open(out_path, 'w')
            dump_ids = dump.ids
            logger.info(f"Found {len(dump_ids)} IDs for {out_filename}")
            logger.debug(dump_ids)
            out_file.write("\n".join(dump_ids))


__main__()
