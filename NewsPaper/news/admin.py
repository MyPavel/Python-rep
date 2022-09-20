from django.contrib import admin
from .models import Post, Author, Category, PostCategory, CategorySubscribers


admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(CategorySubscribers)
