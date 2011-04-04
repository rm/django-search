from blog.blogapp.models import Author, Entry, Tag
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('date', 'title')}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

for class_, admin_ in ((Author, AuthorAdmin),
                       (Entry, EntryAdmin),
                       (Tag, TagAdmin)):
    admin.site.register(class_, admin_)

