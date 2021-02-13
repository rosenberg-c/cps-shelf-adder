import requests
import csv
import re
import sys


def username_auth(server_address, username, password):
    return requests.post(
        server_address + '/login?next=/',
        data={
            'username': username,
            'password': password,
            'submit': '',
            'remember_me': 'on',
            'next': '/'
        }
    )


def add_book_job(server_address, shelf_id, current_row, cookies, headers):
    return requests.get(
        server_address + '/shelf/add/' + shelf_id + '/' + current_row['id'],
        cookies=cookies, headers=headers
    )


def evaluate_job(current_row, shelf_id, job):
    if job.status_code != 200:
        print(
            'Error: Failed to add book with id %s to shelf %s' % (current_row['id'], shelf_id))
    else:
        message = re.findall(u"id=\"flash_.*class=.*>(.*)</div>",
                             job.content.decode('utf-8'))
        if not message:
            print('Error: Book with id %s already in shelf, or shelf not exisitend' % (
                current_row['id']))
        else:
            print('Book with id %s was added to shelf with message: %s' % (
                current_row['id'], message[0]))


def authenticated(auth_i):
    if auth_i.status_code == 200:
        return True
    return False


def get_csv(csv_path):
    if sys.version_info.major >= 3:
        return open(csv_path, newline='', )
    return open(csv_path)


def mass_add_books(args):
    username = args.username
    password = args.password
    shelf_id = args.shelf_id
    csv_path = args.csv_path
    server_address = args.server

    if shelf_id.isdigit():
        _auth = username_auth(server_address=server_address, username=username, password=password)
        if authenticated(auth_i=_auth):
            print("SIGNED IN")
            headers = {'Referer': server_address + '/'}

            with get_csv(csv_path=csv_path) as csv_file:
                reader = csv.DictReader(csv_file)
                for index, current_row in enumerate(reader):
                    if "id" in current_row:
                        if current_row['id'].isdigit():
                            evaluate_job(
                                current_row=current_row,
                                shelf_id=shelf_id,
                                job=add_book_job(
                                    server_address=server_address,
                                    shelf_id=shelf_id,
                                    current_row=current_row,
                                    cookies=_auth.cookies,
                                    headers=headers
                                ),
                            )

                        else:
                            print('Error: id %s is not a number' % current_row['id'])
                    else:
                        print(
                            "No ID-field found in current row of csv file, check for seperation character (has to be ',') and spelling of 'id' field")
                        exit()

        else:
            print('Error: Could not log in to calibre-web')
    else:
        print('Error: Shelf_id is not a number')
