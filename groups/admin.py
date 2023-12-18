from django.contrib import admin
from django.contrib import admin
from .models import Group, GroupUser, GroupSong


admin.site.register(Group)
admin.site.register(GroupUser)
admin.site.register(GroupSong)