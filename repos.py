import os
import time
import progressbar
from src import CliArgs
from src.models.AuthToken import AuthToken
from src.Graphql import Graphql
from dotenv import load_dotenv
from src.models.Repo import Repo
from src.models.GithubException import GithubException
from src import CsvUtils


# Load env file
load_dotenv()

# flush progress bar
progressbar.streams.flush()


def mine_repos():

    # parse arguments
    args = CliArgs.get_args(total=('Total repos to be fetch', 1000),
                            perrequest=('Number of repos per request', 100))

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))

    total_repos = int(args.total)
    repos_per_request = int(args.perrequest)

    graphql = Graphql(url, repos_per_request)

    if total_repos % repos_per_request != 0:
        raise Exception(
            'Repos per request should be divisible by total repos number')

    repo_list: list[Repo] = []

    print('Fetching repos...')

    with progressbar.ProgressBar(max_value=total_repos, redirect_stdout=True) as bar:
        while len(repo_list) < total_repos:
            try:
                print('Fetching cursor: {}'.format(graphql.cursor))
                print('Current token: {}'.format(token.get_token()))

                # Build query
                query = graphql.get_repos_query()

                # Get repos
                repo_data = graphql.get_repos_data(query, token.get_token())

                # add to list
                for repo in [Repo.from_github(repo) for repo in repo_data]:
                    if len(repo_list) == total_repos:
                        break

                    elif repo.pr_count > 100 and not next((r for r in repo_list if r.name_with_owner == repo.name_with_owner), None):
                        CsvUtils.save_list_to_csv(
                            [repo], 'repos.csv', mode='a', header=False)

                        repo_list.append(repo)

                # break if total was reach
                if len(repo_list) == total_repos:
                    break

                bar.update(len(repo_list))

            except GithubException:
                time.sleep(len(repo_list) * 2)
                token.next_token()

    CsvUtils.save_list_to_csv(repo_list, 'final_repos.csv')


if __name__ == '__main__':
    mine_repos()
