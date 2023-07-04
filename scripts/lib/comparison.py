from rule_dump import RuleDump


class Comparison:
    def __init__(self, from_dump: RuleDump, to_dump: RuleDump):
        self.from_dump = from_dump
        self.to_dump = to_dump

    def added(self):
        to_ids = self.to_dump.ids
        from_ids = self.from_dump.ids
        return [i for i in to_ids if i not in from_ids]
