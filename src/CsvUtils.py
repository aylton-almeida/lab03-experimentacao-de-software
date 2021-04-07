import pandas as pd

from src.models.Repo import Repo


def save_repos_to_csv(repos: list[Repo], path: str, mode='w', header=True):
    data_frame = pd.DataFrame([repo.__dict__ for repo in repos])

    data_frame.to_csv(path, mode=mode, header=header)


def read_repos_from_csv(csv: str, delimiter: str = ','):
    data_frame = pd.read_csv(csv, delimiter)

    return [Repo.from_dataframe(row) for index, row in data_frame.iterrows()]
