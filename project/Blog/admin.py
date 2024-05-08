from django.contrib import admin

from .models import CustomUser,Post,likes,UserProfile,Comment


admin.site.register(CustomUser)

admin.site.register(Post)

admin.site.register(likes)

admin.site.register(UserProfile)

admin.site.register(Comment)
 