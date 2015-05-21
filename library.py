# coding=utf-8


"""
GOAL: Use object-oriented Python to model a public library (w/ three classes:
Library, Shelf, & Book). The library should be aware of a number of shelves.
Each shelf should know what books it contains. Make the book object have
"enshelf" and "unshelf" methods that control what shelf the book is sitting on.
The library should have a have a method to report all books it contains. Note:
this should *not* be a Django (or any other) app - just a single file with
three classes (pls commands at the bottom showing it works) is all that is
needed. In addition to pushing this Python file to your Github account, please
also setup a repl.it account and enter the saved URL.
"""

import copy


class Library(object):
    """A class for a library."""
    def __init__(self, name):
        self.name = name
        self.shelves = []

    def add_shelf(self, name):
        shelf = Shelf(name)
        self.shelves.append(shelf)
        return shelf

    def report_books(self):
        """Report all books in library."""
        for shelf in self.shelves:
            for book in shelf.books:
                print(book.title)


class Shelf(object):
    """A class for shelves in a library."""
    def __init__(self, name):
        self.name = name
        self.books = {}


class Book(object):
    """A class for books."""
    def __init__(self, title="", author="", copy=1, status="Checked In",
                 due="", shelf=None, **kwargs):
        self.title = title
        self.author = author
        self.copy = copy
        self.status = status
        self.due = due
        self.shelf = shelf
        self.details = kwargs

    @property
    def book_id(self):
        return (
            "{title} c.{copy}".format(title=self.title, copy=self.copy)
        )

    def enshelf(self, shelf):
        """Add a book to a shelf."""
        if self.book_id not in shelf.books:
            self.shelf = shelf
            shelf.books[self.book_id] = self
        else:
            print("Book already in shelf.")

    def unshelf(self):
        """Remove a book from its shelf."""
        if self.shelf:
            self.shelf.books.pop(self.book_id)
            self.shelf = None

    def check_out(self, due=""):
        """Check out book from library."""
        self.unshelf()
        self.enshelf(checked_out)
        self.status = "Checked Out"
        self.due = due

    def add_copy(self):
        new_copy = copy.deepcopy(self)
        new_copy.shelf = None
        new_copy.copy += 1
        new_copy.enshelf(self.shelf)

library = Library("Lake City Public Library")

checked_out = library.add_shelf("Checked Out")
shelf1 = library.add_shelf("Shelf 1")
shelf2 = library.add_shelf("Shelf 2")
shelf3 = library.add_shelf("Shelf 3")

book1 = Book(
    title="The Scar",
    author="Virginia Wolfe",
    call_num="332.024 R3903o 2015",
    ISBN=9781591847557,
    page_count=211
)

book2 = Book(
    title="Winning",
    author="Charlie Sheen",
    call_num="364.989 R3903o 2010",
    ISBN=9783434147557,
    page_count=150
)

book3 = Book(
    title="Wounded",
    author="Jim Bush",
    call_num="334.053 R3903o 2014",
    ISBN=9781593434427,
    page_count=100
)
