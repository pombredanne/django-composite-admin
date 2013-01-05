from django.db import models


class Author(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    bio = models.TextField()

    def __unicode__(self):
        return '%s %s' % (self.firstname, self.lastname)


class Poem(models.Model):
    TRIPHOP = 1
    HIPHOP = 2
    POETRY = 3
    ROCK = 4
    SLAM = 5

    KIND_CHOICES = (
        (TRIPHOP, 'Triphop'),
        (HIPHOP, 'Hiphop'),
        (POETRY, 'Poetry'),
        (ROCK, 'Rock'),
        (SLAM, 'Slam'),
    )

    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(Author)
    has_sound = models.BooleanField()
    has_record = models.BooleanField()
    kind = models.PositiveIntegerField(choices=KIND_CHOICES)

    def __unicode__(self):
        return self.title
