from django.db import models
from django.db.models import Count


class Library(models.Model):
    name = models.CharField(max_length=100)

    def get_author_count(self):
        return self.book_set.values_list('author', flat=True).distinct().count()

    def get_book_count(self):
        return self.book_set.count()

    class Meta:
        ordering = ('name',)


class Book(models.Model):
    title = models.CharField(db_index=True, max_length=100)
    author = models.ForeignKey('book.Author', on_delete=models.CASCADE)
    libraries = models.ManyToManyField('book.Library')

    def get_libraries_names(self):
        library_names = list(
            self.libraries
            .values_list('name', flat=True)
            .order_by('name'))

        return ", ".join(library_names)

    class Meta:
        ordering = ('-title',)


class Author(models.Model):
    first_name = models.CharField(db_index=True, max_length=100)
    last_name = models.CharField(db_index=True, max_length=100)

    @property
    def fullname(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_book_count(self):
        return self.book_set.count()

    class Meta:
        ordering = ('first_name', 'last_name')
