from src.models.GithubException import GithubException
import requests
import json

from requests.models import Response


class Graphql:

    url: str
    items_per_request: int
    cursor = None

    def __init__(self, url: str, items_per_request: int) -> None:
        self.url = url
        self.items_per_request = items_per_request

    def get_repos_query(self, stars: str = '>100'):
        return """
               query {
                 search(type: REPOSITORY, first: %(repos)i, query: "stars:%(stars)s", after: %(after)s) {
                   edges {
                     cursor
                     node {
                       ... on Repository {
                         nameWithOwner
                         name
                         url
                         stargazerCount
                         pullRequests(states: [CLOSED,MERGED]) {
                           totalCount
                         }
                       }
                     }
                   }
                 }
               }
               """ % {
            'repos': self.items_per_request,
            'stars': stars,
            'after': ('"{}"'.format(self.cursor) if self.cursor else 'null')
        }

    def get_prs_query(self, owner: str, name: str):
        return """
               query {
                 repository(owner: "%(owner)s", name: "%(name)s") {
                   pullRequests(first: %(prs)i, states: [CLOSED,MERGED], after: %(after)s) {
                     pageInfo {
                       hasNextPage
                     }
                     edges {
                       cursor
                       node {
                         ... on PullRequest {
                           state
                           createdAt
                           mergedAt
                           closedAt
                           changedFiles
                           body
                           participants {
                             totalCount
                           }
                           reviews {
                             totalCount
                           }
                         }
                       }
                     }
                   }
                 }
               }
               """ % {
            'owner': owner,
            'name': name,
            'prs': self.items_per_request,
            'after': ('"{}"'.format(self.cursor) if self.cursor else 'null')
        }

    def _fetch_data(self, query: str, token: str) -> dict:
        response: Response = requests.post(self.url, json={'query': query}, headers={
            'Authorization': token
        })

        if response.status_code != 200:
            raise GithubException(
                'There was an error while trying to make the request'
            )

        return json.loads(response.text)

    def get_repos_data(self, query: str, token: str):

        json_data = self._fetch_data(query, token)

        edges: list = json_data['data']['search']['edges']

        if len(edges) < self.items_per_request:
            self.cursor = None

        else:
            self.cursor = edges[-1]['cursor']

        return edges

    def get_pr_data(self, query: str, token: str):

        json_data = self._fetch_data(query, token)

        prs = json_data['data']['repository']['pullRequests']

        has_next_page = prs['pageInfo']['hasNextPage']
        edges: list = prs['edges']

        if not has_next_page:
            self.cursor = None
        else:
            self.cursor = edges[-1]['cursor']

        return edges, has_next_page
