from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from book.models import Book, Author, Library


class LoginRequired:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BookListView(LoginRequired, ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'books'


class AuthorListView(LoginRequired, ListView):
    model = Author
    paginate_by = 10
    context_object_name = 'authors'


class LibraryListView(LoginRequired, ListView):
    model = Library
    paginate_by = 10
    context_object_name = 'libraries'
