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
               query example {
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

    def get_repos_data(self, query: str, token: str):
        response: Response = requests.post(self.url, json={'query': query}, headers={
            'Authorization': token
        })

        if response.status_code != 200 or 'errors' in response.text:
            print(response.text)
            raise GithubException(
                'There was an error while trying to make the request'
            )

        json_data: dict = json.loads(response.text)

        edges: list = json_data['data']['search']['edges']

        if len(edges) < self.items_per_request:
            self.cursor = None

        else:
            self.cursor = edges[-1]['cursor']

        return edges
