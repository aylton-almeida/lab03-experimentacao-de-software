from __future__ import annotations

from datetime import datetime


class PullRequest:

    cursor: str
    name_with_owner: str
    state: str
    created_at: datetime
    merged_at: datetime
    closed_at: datetime
    review_time: int
    changed_files: int
    body_size: str
    participants_count: int
    reviews_count: int

    def __init__(self, data: dict) -> None:
        self.cursor = data.get('cursor')
        self.name_with_owner = data.get('nameWithOwner')
        self.state = data.get('state')
        self.created_at = datetime.fromisoformat(
            data.get('createdAt').replace('Z', '+00:00'))
        self.merged_at = datetime.fromisoformat(
            data.get('mergedAt').replace('Z', '+00:00')) if data.get('mergedAt') else None
        self.closed_at = datetime.fromisoformat(
            data.get('closedAt').replace('Z', '+00:00'))
        self.review_time = int(
            ((self.closed_at - self.created_at).seconds) // 3600)
        self.changed_files = data.get('changedFiles')
        self.body_size = len(data.get('body'))
        self.participants_count = data.get('participantsCount')
        self.reviews_count = data.get('reviewsCount')

    @staticmethod
    def from_github(data: dict, name_with_owner: str) -> PullRequest:
        node = data.get('node')

        return PullRequest({
            'cursor': data.get('cursor'),
            'nameWithOwner': name_with_owner,
            'state': node.get('state'),
            'createdAt': node.get('createdAt'),
            'mergedAt': node.get('mergedAt'),
            'closedAt': node.get('closedAt'),
            'changedFiles': node.get('changedFiles'),
            'body': node.get('body'),
            'participantsCount': node.get('participants').get('totalCount'),
            'reviewsCount': node.get('reviews').get('totalCount'),
        })
