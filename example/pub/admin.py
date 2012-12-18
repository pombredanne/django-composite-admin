from django.contrib import admin as oldadmin

from models import Author
from models import Haiku

from newadmin import admin as newadmin


newadmin.register(Author)
newadmin.register(Haiku)

oldadmin.site.register(Author)
oldadmin.site.register(Haiku)
