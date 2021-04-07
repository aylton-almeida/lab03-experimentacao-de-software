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
    args = CliArgs.get_args(initialrepo=('Initial repo index', 0))

    # Get env variables
    url = os.getenv('API_URL')
    token = AuthToken(os.getenv('AUTH_TOKENS').split(','))

    initial_repo = int(args.initialrepo)

    graphql = Graphql(url, 100)

    # read repos csv
    repo_list = CsvUtils.read_repos_from_csv('final_repos.csv')

    trimmed_repos = repo_list[initial_repo:]

    print('Fetching repos...')

    # extremely necessary progress bar for better user experience
    with progressbar.ProgressBar(max_value=len(trimmed_repos), redirect_stdout=True) as bar:
        for index in range(len(trimmed_repos)):
            repo = trimmed_repos[index]

            print('Fetching PRs for Repo {}'.format(repo.name_with_owner))

            bar.update(index)


if __name__ == '__main__':
    mine_repos()
