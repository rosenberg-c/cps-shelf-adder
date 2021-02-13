from mass_add_books import mass_add_books
from lib.argvs import get_argvs

if __name__ == '__main__':
    mass_add_books(
        args=get_argvs()
    )

"""
Uses csv name to create shelf

example: [ shelf name = lib ]

python main.py \
 --username user \
 --password user123 \
 --csv-path /path/to/lib.csv \
 --server http://server:8083 \
 --create-shelf \
 --public-shelf

"""