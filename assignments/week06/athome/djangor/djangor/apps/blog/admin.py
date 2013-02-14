from django.contrib import admin
from djangor.apps.blog.models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(BlogPost)
