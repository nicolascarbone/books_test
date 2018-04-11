from django.contrib.auth.models import User
from django.test import TestCase, Client
from pyquery import PyQuery as pq

from book.models import Author, Book, Library


class BookTestCase(TestCase):

    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'

        self.user = User.objects.create_user(
            username=self.username,
            password=self.password)

        self.author = Author.objects.create(
            first_name='Django',
            last_name='Test')

        self.library = Library.objects.create(
            name='MyLibrary'
        )

        zen_book = Book.objects.create(author=self.author, title='Zen')
        zen_book.libraries.add(self.library)
        awesome_book = Book.objects.create(author=self.author, title='Awesome')
        awesome_book.libraries.add(self.library)
        self.books = [zen_book, awesome_book]

        self.client = Client()
        self.guest_client = Client()
        self.client.login(username=self.username, password=self.password)
        self.urls = ['/book/', '/author/', '/library/']

    def test_views_cannot_accessible_by_guest_user(self):
        for url in self.urls:
            response = self.guest_client.get(url)
            self.assertNotEqual(200, response.status_code)

    def test_logged_user_can_access_to_views(self):
        for url in self.urls:
            response = self.client.get(url)
            self.assertEqual(200, response.status_code)

    def test_ensure_book_ordering(self):
        response = self.client.get(self.urls[0])
        dom = pq(response.content)
        tr = dom('table tbody tr')
        self.assertEqual(tr.length, len(self.books))
        td1 = dom('table tbody tr:first td:first').html()
        td2 = dom('table tbody tr:last td:first').html()
        self.assertGreaterEqual(td1, td2)

    def test_author_book_count(self):
        initial_book_count = self.author.get_book_count()
        self.books.append(Book.objects.create(
            author=self.author,
            title='New Book'))
        new_book_count = self.author.get_book_count()
        self.assertLess(initial_book_count, new_book_count)

    def test_library_book_count(self):
        initial_book_count = self.library.get_book_count()

        book = Book.objects.create(
            author=self.author,
            title='New Book')
        book.libraries.add(self.library)
        self.books.append(book)

        new_book_count = self.library.get_book_count()
        self.assertLess(initial_book_count, new_book_count)

    def test_library_author_count(self):

        initial_author_count = self.library.get_author_count()

        # Create a book for the same author, count should remains the same
        book = Book.objects.create(
            author=self.author,
            title="Same Author's Book")
        book.libraries.add(self.library)
        partial_author_count = self.library.get_author_count()
        self.assertEqual(initial_author_count, partial_author_count)

        # Create a book for a new author, count should  increment by 1
        new_author = Author.objects.create(
            first_name='Nicolas',
            last_name='Carbone'
        )

        book = Book.objects.create(
            author=new_author,
            title="Nico's Book")
        book.libraries.add(self.library)
        new_author_count = self.library.get_author_count()
        self.assertLess(initial_author_count, new_author_count)
