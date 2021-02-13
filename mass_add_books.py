import os

from lib.auth import username_auth, authenticated
from app.shelves import create_shelf, add_to_shelf, delete_shelf, get_shelves


def sync_add(server_address, cookies, shelf_name, should_be_public_shelf, csv_path):
    print("Create shelf")
    new_id = create_shelf(
        server_address=server_address,
        cookies=cookies,
        shelf_name=shelf_name,
        should_be_public_shelf=should_be_public_shelf
    )
    print("Created shelf with id: " + new_id)
    add_to_shelf(
        csv_path=csv_path,
        shelf_id=new_id,
        server_address=server_address,
        cookies=cookies,
    )


def sync_with_shelf(csv_path, shelf_id, server_address, cookies, shelf_name, public_shelf):
    data = delete_shelf(
        shelf_id=shelf_id,
        server_address=server_address,
        cookies=cookies,
    )

    if data.status_code == 200:
        print("Removed shelf")
    else:
        print("Could not remove shelf")
        exit()

    sync_add(
        csv_path=csv_path,
        server_address=server_address,
        cookies=cookies,
        shelf_name=shelf_name,
        should_be_public_shelf=public_shelf
    )


def mass_add_books(args):
    server_address = args.server
    username = args.username
    password = args.password

    csv_path = args.csv_path

    should_create_shelf = args.create_shelf
    should_be_public_shelf = args.public_shelf

    if args.shelf_name is not None:
        shelf_name = args.shelf_name
    else:
        shelf_name = os.path.split(args.csv_path)[1].split(".")[0]

    _auth = username_auth(
        server_address=server_address,
        username=username,
        password=password
    )

    if authenticated(auth=_auth):
        print("SIGNED IN")

        _shelves = get_shelves(
            server_address=server_address,
            cookies=_auth.cookies,
        )

        shelf_existing = False

        for s in _shelves:
            if shelf_name in s["name"]:
                shelf_existing = True

        if shelf_existing:
            for s in _shelves:
                if s["name"] == shelf_name:
                    sync_with_shelf(
                        csv_path=csv_path,
                        shelf_id=s["id"],
                        server_address=server_address,
                        cookies=_auth.cookies,
                        shelf_name=shelf_name,
                        public_shelf=should_be_public_shelf
                    )

        if shelf_existing is False and should_create_shelf is True:
            print("Sync add")
            sync_add(
                csv_path=csv_path,
                server_address=server_address,
                cookies=_auth.cookies,
                shelf_name=shelf_name,
                should_be_public_shelf=should_be_public_shelf
            )
        print("End")
    else:
        print('Error: Could not log in to calibre-web')
