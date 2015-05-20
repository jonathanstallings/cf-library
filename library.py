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


class Library(object):
    """docstring for Library"""
    def __init__(self, name):
        self.name = name
        self._shelves = {}

    def report_books(self):
        """Report all books in library."""
        pass


class Shelf(object):
    """docstring for Shelf"""
    def __init__(self, name):
        self.name = name
        self._books = {}


class Book(object):
    """docstring for Book"""
    def __init__(self, title="", author="", call_num="", copies=1, **kwargs):
        self.title = title
        self.author = author
        self.call_num = call_num
        self._copies = copies
        self.details = {}

        for data in kwargs:
            self.details[data] = kwargs[data]

    def enshelf(self, shelf):
        """Add a book to a shelf."""
        pass

    def unshelf(self):
        """Remove a book from its shelf."""
        pass
