from django.contrib import admin as oldadmin

from models import Author
from models import Poem

oldadmin.site.register(Author)
oldadmin.site.register(Poem)
