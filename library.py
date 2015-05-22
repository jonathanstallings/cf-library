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
import datetime


def show_logo():
    """Print out the library logo."""
    logo = (
        " _      _ _                          \n"
        "| |    (_) |                         \n"
        "| |     _| |__  _ __ __ _ _ __ _   _ \n"
        "| |    | | '_ \| '__/ _` | '__| | | |\n"
        "| |____| | |_) | | | (_| | |  | |_| |\n"
        "|______|_|_.__/|_|  \__,_|_|   \__, |\n"
        "                                __/ |\n"
        "                               |___/ \n"
    )
    print logo


def set_due_date(days=0, weeks=0):
    """
    Set a due date based on time delta in days or weeks from today.

    Args:
        days: time delta in days from today
        weeks: time delt in weeks from today

    Returns: Due date in datetime format
    """
    today = datetime.date.today()
    due_date = today + datetime.timedelta(days=days, weeks=weeks)
    return due_date


class Library(object):
    """A class for a library."""
    def __init__(self, name):
        self.name = name
        self.shelves = []

    def __str__(self):
        return "{name}".format(name=self.name)

    def add_shelf(self, name):
        """
        Create a new shelf object and add it to the library.

        Args:
            name: the name for the shelf object

        Returns: the newly created shelf object
        """
        shelf = Shelf(name, self)
        self.shelves.append(shelf)
        return shelf

    def remove_shelf(self, shelf):
        """
        Remove a shelf object from the library.

        Args:
            shelf: the shelf object to remove
        """
        self.shelves.remove(shelf)

    def get_shelf(self, index):
        """
        Return a given shelf object from library by index.

        Args:
            index: the index of the shelf

        Returns: the shelf object
        """
        return self.shelves[index]

    def report(self):
        """Report all books in library in tabular format."""
        print("{library} Inventory\n".format(library=self))
        print(
            "{:^20} | {:^20} | {:^10} | {:^20}\n"
            .format("Title", "Author", "Status", "Due Date")
        )
        for shelf in self.shelves[1:]:
            shelf.report()
        checked_out.report()


class Shelf(object):
    """A class for shelves in a library."""
    def __init__(self, name, library=None):
        self.name = name
        self.library = library
        self.books = {}

    def __str__(self):
        return (
            "{index}. {name}"
            .format(index=self.library.shelves.index(self), name=self.name)
        )

    def add_books(self, *args):
        """
        Add books objects to shelf.

        Args: Any number of book objects
        """
        for book in args:
            book.enshelf(self)

    def remove_books(self, *args):
        """
        Remove book objects from shelf.

        Args: Any number of book objects
        """
        for book in args:
            if book.book_id in self.books:
                book.unshelf()

    def get_book(self, book_id):
        """
        Return a given book object from shelf by book id.

        Args:
            book_id: the book_id of the book

        Returns: the book object
        """
        return self.books[book_id]

    def report(self):
        """Report books on shelf in tabular format."""
        print("{:_<80}".format(self))
        for book in self.books.itervalues():
            book.report()
        print("\n")


class Book(object):
    """A class for books."""
    def __init__(self, title="", author="", copy=1, due=None, shelf=None,
                 **kwargs):
        """
        Initialize a new book object. Beyond the set attributes, Any number of
        additional keyword argmuments can be passed to store more detailed
        book information in the details dictionary.
        """
        self.title = title
        self.author = author
        self.copy = copy
        self.status = "Checked In"
        self.due_date = due
        self.shelf = shelf
        self.last_shelf = shelf
        self.details = kwargs

    @property
    def book_id(self):
        """Create unique id for book to store in shelf books dictionary."""
        return (
            "{title} c.{copy}".format(title=self.title, copy=self.copy)
        )

    @property
    def status(self):
        """Check and return book status."""
        today = datetime.date.today()
        if self.due_date and self.due_date < today:
            return "Overdue"
        else:
            return self._status

    @status.setter
    def status(self, status):
        self._status = status

    def __str__(self):
        return (
            "Title: {title}\n"
            "Author: {author}\n"
            "Copy: {copy} of {total}\n"
            "Status: {status}\n"
            "Due Date: {due_date}\n"
            .format(
                title=self.title,
                author=self.author,
                copy=self.copy, total=self.get_latest_copy(),
                status=self.status,
                due_date=self.due_date
            )
        )

    def show_details(self):
        """Show detailed book information."""
        print self
        for key, value in self.details.iteritems():
            print("{k}: {v}".format(k=key, v=value))

    def report(self):
        """Report basic book info in tabular format."""
        print(
            "{:<20} | {:<20} | {:<10} | {}"
            .format(self.book_id, self.author, self.status, self.due_date)
        )

    def enshelf(self, shelf):
        """
        Add a book to a shelf.

        Args:
            shelf: the shelf object destination
        """
        if self.shelf == shelf:
            print("Book already in shelf.")
        elif self.book_id in shelf.books:
            print("The same copy is already on the shelf!")
        else:
            self.unshelf()
            self.shelf = shelf
            shelf.books[self.book_id] = self

    def unshelf(self):
        """Remove a book from its shelf."""
        if self.shelf:
            self.shelf.books.pop(self.book_id)
            self.last_shelf = self.shelf
            self.shelf = None

    def reshelf(self):
        """Add a book to its last visited shelf."""
        if self.last_shelf:
            self.enshelf(self.last_shelf)
        else:
            print("Cannot reshelf: no previous shelf on record.")

    def checkout(self, days=0, weeks=2):
        """
        Check out book from library, defaulting to 2 weeks from today.

        Args:
            days: time delta in days from today
            weeks: time delt in weeks from today
        """
        self.enshelf(checked_out)
        self.status = "Checked Out"
        self.due_date = set_due_date(days=days, weeks=weeks)

    def checkin(self):
        """Check in and reshelf book to library."""
        self.reshelf()
        self.status = "Checked In"
        self.due_date = None

    def get_latest_copy(self, search_lib=None):
        """
        Return the lastest copy number of a title in a library.

        Args:
            search_lib: the library to search (defaults to current library)

        Returns: the latest copy number (int)
        """
        latest_copy = 1
        try:
            library_to_search = search_lib or self.shelf.library
        except AttributeError:
            print("Not currently part of a library!\n")
        else:
            for shelf in library_to_search.shelves:
                for book in shelf.books.values():
                    if book.title == self.title and book.copy > latest_copy:
                        latest_copy = book.copy
        finally:
            return latest_copy

    def add_copies(self, copy_num=1):
        """
        Add a given number of book copies to same location.

        Args:
            copy_num: the number of additional copies (default 1)

        Returns: a list of the new book copies.
        """
        results = []
        for x in range(copy_num):
            new_book_copy = copy.deepcopy(self)
            new_book_copy.shelf = None
            new_book_copy.copy = self.get_latest_copy() + 1
            new_book_copy.enshelf(self.shelf)
        return results


# if __name__ == '__main__':
show_logo()
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

book4 = Book(
    title="Unbowed",
    author="Sean Ramses",
    call_num="323.054 T3433o 1978",
    ISBN=9781343534556,
    page_count=565
)

book1.enshelf(shelf1)
book2.enshelf(shelf2)
shelf3.add_books(book3, book4)

book1.add_copies(2)
book1.checkout()

library.report()
