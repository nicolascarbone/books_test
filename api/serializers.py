from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import serializers, exceptions

from book.models import Book, Author, Library


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'fullname')


class BookSerializer(serializers.ModelSerializer):
    author_fullname = serializers.CharField(source='author.fullname')
    libraries = serializers.SerializerMethodField()

    def get_libraries(self, obj):
        return obj.get_libraries_names()

    class Meta:
        model = Book
        fields = ('title', 'author_fullname', 'libraries')


class LibrarySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()
    author_count = serializers.SerializerMethodField()

    def get_book_count(self, obj):
        return obj.get_book_count()

    def get_author_count(self, obj):
        return obj.get_author_count()

    class Meta:
        model = Library
        fields = ('name', 'book_count', 'author_count')
