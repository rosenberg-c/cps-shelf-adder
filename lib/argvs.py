import argparse


def get_argvs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', dest='username', type=str, required=True)
    parser.add_argument('--password', dest='password', type=str, required=True)
    parser.add_argument('--shelf-id', dest='shelf_id', type=str, required=False)
    parser.add_argument('--shelf-name', dest='shelf_name', type=str, required=False)
    parser.add_argument('--csv-path', dest='csv_path', type=str, required=True)
    parser.add_argument('--server', dest='server', type=str, required=True)
    parser.add_argument('--create-shelf', action="store_true", required=False, default=False)
    parser.add_argument('--public-shelf', action="store_true", required=False, default=False)

    return parser.parse_args()
