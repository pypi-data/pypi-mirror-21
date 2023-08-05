from __future__ import absolute_import, division, print_function, unicode_literals

import random

from amaascore.books.book import Book
from amaascore.tools.helpers import random_string


def generate_book(asset_manager_id=None, book_id=None, owner_id=None, party_id=None, book_type='Trading'):

    book = Book(asset_manager_id=asset_manager_id or random.randint(1, 1000),
                book_id=book_id or random_string(10),
                book_type=book_type,
                owner_id=owner_id or random.randint(1, 1000),
                party_id=party_id or random_string(10))  # Can also be the asset_manager_id of the book

    return book
