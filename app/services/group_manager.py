from typing import Dict, List

class GroupManager:
    def __init__(self):
        self.groups: Dict[str, List[str]] = {}

    def create_group(self, group_name: str):
        if group_name not in self.groups:
            self.groups[group_name] = []

    def add_user_to_group(self, group_name: str, username: str):
        if group_name in self.groups:
            self.groups[group_name].append(username)

    def remove_user_from_group(self, group_name: str, username: str):
        if group_name in self.groups:
            self.groups[group_name].remove(username)

    def get_group_members(self, group_name: str) -> List[str]:
        return self.groups.get(group_name, [])

group_manager = GroupManager()
