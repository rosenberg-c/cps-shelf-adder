import argparse

username = 'admin'
password = ''
shelf_id = '1'
booklist = 'booklist.csv'
serveradress = 'http://127.0.0.1:8083'


def get_argvs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', dest='username', type=str, required=True)
    parser.add_argument('--password', dest='password', type=str, required=True)
    parser.add_argument('--shelf-id', dest='shelf_id', type=str, required=True)
    parser.add_argument('--csv-path', dest='csv_path', type=str, required=True)
    parser.add_argument('--server', dest='server', type=str, required=True)

    args = parser.parse_args()
    return args
