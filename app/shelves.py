import csv

import requests
import re

from lib.csvs import open_csv


def evaluate_job(current_row, shelf_id, job):
    if job.status_code != 200:
        print(
            'Error: Failed to add book with id %s to shelf %s' % (current_row['id'], shelf_id))
    else:
        message = re.findall(u"id=\"flash_.*class=.*>(.*)</div>",
                             job.content.decode('utf-8'))[0].replace("Book has been added to shelf: ", "")
        if not message:
            print('Error: Book with id %s already in shelf, or shelf not exisitend' % (
                current_row['id']))
        else:
            print('Book id %s: added to: %s' % (
                current_row['id'], message))


def add_to_shelf(csv_path, shelf_id, server_address, cookies):
    with open_csv(csv_path=csv_path) as csv_file:
        for current_row in csv.DictReader(csv_file):
            if "id" in current_row:
                if current_row['id'].isdigit():
                    evaluate_job(
                        current_row=current_row,
                        shelf_id=shelf_id,
                        job=add_book(
                            server_address=server_address,
                            shelf_id=shelf_id,
                            current_row=current_row,
                            cookies=cookies,
                        ),
                    )
                else:
                    print('Error: id %s is not a number' % current_row['id'])
            else:
                print(
                    "No ID-field found in current row of csv file, check for seperation character (has to be ',') and spelling of 'id' field")


def add_book(server_address, shelf_id, current_row, cookies):
    headers = {'Referer': server_address + '/'}
    return requests.get(
        server_address + '/shelf/add/' + shelf_id + '/' + current_row['id'],
        cookies=cookies,
        headers=headers
    )


def get_shelves(server_address, cookies):
    headers = {'Referer': server_address + '/'}

    _job = requests.get(
        server_address,
        cookies=cookies,
        headers=headers
    )

    _found = re.findall(
        u"<a href=\"/shelf/.*class=\"glyphicon.*\"></span>.*</a>",
        _job.content.decode('utf-8')
    )

    _shelves = []
    _is_puplic = False
    for f in _found:
        _id_name = f \
            .replace("<a href=\"/shelf/", "") \
            .replace("\"><span class=\"glyphicon glyphicon-list shelf\"></span>", "__--__") \
            .replace("</a>", "")
        if " (Public)" in _id_name:
            _is_puplic = True
        _id, _name = _id_name.replace(" (Public)", "").split("__--__")
        _shelves.append({"id": _id, "name": _name, "is_public": _is_puplic})
    return _shelves


def delete_shelf(server_address, cookies, shelf_id):
    headers = {'Referer': server_address + '/'}
    return requests.get(
        server_address + "/shelf/delete/" + shelf_id,
        cookies=cookies,
        headers=headers
    )


def create_shelf(server_address, cookies, shelf_name, should_be_public_shelf):
    headers = {'Referer': server_address + '/'}

    if should_be_public_shelf:
        data = dict(title=shelf_name, is_public="any-value_only-key-is-relevant")
    else:
        data = dict(title=shelf_name)

    _job = requests.post(
        server_address + "/shelf/create",
        cookies=cookies,
        headers=headers,
        data=data
    )
    already_exist = re.findall(
        u"class=\"alert alert-danger\">A public shelf with the name ",
        _job.content.decode('utf-8'))
    if len(already_exist) != 0:
        print("A public shelf already exist: " + shelf_name)
        print("Try enabling \"Allow Editing Public Shelves\"")
        exit()
    id_dirty = re.findall(
        u"<a id=\"edit_shelf\" href=\"/shelf/edit/.*\" class=\"",
        _job.content.decode('utf-8'))[0]
    return id_dirty.split("href=\"/shelf/edit/")[1].split("\" class")[0]
