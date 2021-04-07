from __future__ import annotations

from pandas.core.series import Series


class Repo:

    cursor: str
    name_with_owner: str
    name: str
    url: str
    stargazer_count: str
    pr_count: int

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.name_with_owner = data.get('nameWithOwner')
        self.name = data.get('name')
        self.url = data.get('url')
        self.stargazer_count = data.get('stargazerCount')
        self.pr_count = data.get('prCount')

    @staticmethod
    def from_github(data: dict) -> Repo:
        node = data.get('node')

        return Repo({
            'cursor': data.get('cursor'),
            'nameWithOwner': node.get('nameWithOwner'),
            'name': node.get('name'),
            'url': node.get('url'),
            'stargazerCount': node.get('stargazerCount'),
            'prCount': int(node.get('pullRequests').get('totalCount'))
        })

    @staticmethod
    def from_dataframe(data: Series) -> Repo:
        return Repo({
            'cursor': data['cursor'],
            'nameWithOwner': data['name_with_owner'],
            'name': data['name'],
            'url': data['url'],
            'stargazerCount': data['stargazer_count'],
            'prCount': data['pr_count']
        })
