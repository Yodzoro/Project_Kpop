from django.contrib import admin
from .models import News, Author

admin.site.register(Author)
admin.site.register(News)