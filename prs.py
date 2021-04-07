import os
from src.models.PullRequest import PullRequest
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
    args = CliArgs.get_args(initialrepo=('Initial repo index', 0), file=(
        'File in witch to save the results', 'prs.csv'))

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))

    initial_repo = int(args.initialrepo)
    file = args.file

    graphql = Graphql(url, 100)

    # read repos csv
    repo_list = CsvUtils.read_repos_from_csv('final_repos.csv')

    trimmed_repos = repo_list[initial_repo:]

    print('Fetching repos...')

    pr_list: list[PullRequest] = []

    # extremely necessary progress bar for better user experience
    with progressbar.ProgressBar(max_value=len(trimmed_repos), redirect_stdout=True) as bar:
        for index in range(len(trimmed_repos)):
            repo = trimmed_repos[index]

            print('Fetching PRs for Repo {}, index {}'.format(
                repo.name_with_owner, index))

            # reset cursor
            graphql.cursor = None

            has_next_page = True
            while has_next_page:
                try:
                    print('Fetching cursor: {}'.format(graphql.cursor))

                    # get query
                    owner, name = repo.name_with_owner.split('/')
                    query = graphql.get_prs_query(owner, name)

                    # fetch prs
                    prs, has_next_page = graphql.get_pr_data(
                        query, token.get_token())

                    # filter prs
                    for pr in prs:
                        pull_request = PullRequest.from_github(
                            pr, repo.name_with_owner)

                        if pull_request.reviews_count > 0 and pull_request.review_time > 1:
                            pr_list.append(pull_request)

                            CsvUtils.save_list_to_csv(
                                [pull_request], file, mode='a', header=False)

                except GithubException:
                    time.sleep(len(pr_list) * 2)
                    token.next_token()
            bar.update(index)


if __name__ == '__main__':
    mine_repos()
