import argparse


def get_args(**kwargs):
    """Generate cli args

    Arguments:
        kwargs[dict]: Pair value in which key is the arg and value a tuple with the help message and default value 

    Returns:
        Namespace: Args namespace object
    """

    parser = argparse.ArgumentParser()

    for key, (help, default) in kwargs.items():
        parser.add_argument("--{}".format(key), help=help, default=default)

    return parser.parse_args()
