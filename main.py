from mass_add_books import mass_add_books
from argvs import get_argvs

username = 'admin'
password = ''
shelf_id = '1'
booklist = 'booklist.csv'
serveradress = 'http://127.0.0.1:8083'

if __name__ == '__main__':
    mass_add_books(
        args=get_argvs()
    )
