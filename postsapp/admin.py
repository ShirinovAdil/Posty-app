from django.contrib import admin
from postsapp.models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)