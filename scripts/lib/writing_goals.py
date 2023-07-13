from typing import List
from elements import ToneTag
from constants import *


class WritingGoal:
    # This constructor isn't needed for now tbh
    def __init__(self, name: str):
        self.name = name
        self.tags = WRITING_GOAL_MAPPING[name]

    @staticmethod
    # From a list of tone tags, return all the writing goals serviced by that tag
    def list_from_tags(tags: List[ToneTag]):
        goals = []
        for tag in tags:
            for goal, tag_list in WRITING_GOAL_MAPPING.items():
                if tag.tag in tag_list and goal not in goals:
                    goals.append(goal)
        return goals
