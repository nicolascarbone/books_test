from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from book.models import Book, Author, Library
from api.serializers import AuthorSerializer, BookSerializer, \
    LibrarySerializer


class TokenViewSet(ObtainAuthToken):
    """
    Returns a fresh token for user with passed id credentials.
    """
    def post(self, request, pk=None):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
        })


class AuthorViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class LibraryViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all libraries.
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
