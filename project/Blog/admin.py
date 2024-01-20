from django.contrib import admin

from .models import CustomUser,Post,likes,dashboard


admin.site.register(CustomUser)

admin.site.register(Post)

admin.site.register(likes)

admin.site.register(dashboard)
