import requests


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


def authenticated(auth):
    if auth.status_code == 200:
        return True
    return False
