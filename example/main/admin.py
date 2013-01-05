from django.contrib import admin as oldadmin

import adminnext

from models import Author
from models import Poem


for admin in (oldadmin, adminnext):

    class AuthorAdmin(admin.ModelAdmin):
        list_display = ('firstname', 'lastname')
        list_editable = ('lastname',)

    class PoemAdmin(admin.ModelAdmin):
        list_display = ('title', 'author', 'kind', 'has_sound', 'has_record')
        list_filter = ('kind', 'author')
        list_editable = ('kind', 'has_sound', 'has_record')

    admin.site.register(Author, AuthorAdmin)
    admin.site.register(Poem, PoemAdmin)
