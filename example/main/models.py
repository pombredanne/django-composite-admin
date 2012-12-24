from django.db import models


class Author(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return '%s %s' % (self.firstname, self.lastname)


class Poem(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(Author)

    def __str__(self):
        return self.title
