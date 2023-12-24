from django.views import View
from django.views.generic import TemplateView

from django.shortcuts import render
from library.models import Song, SongUrl
from groups.models import Group, GroupUser

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        favorite_songs = Song.objects.select_related('songurl').filter(usersong__favorite=True, usersong__user=request.user)
        created_songs = Song.objects.select_related('songurl').filter(created=request.user)


        user_group_ids = GroupUser.objects.filter(user=request.user).values_list('group_id', flat=True)
        user_groups = Group.objects.filter(id__in=user_group_ids)

        context = {
            'favorite_songs': favorite_songs,
            'created_songs': created_songs,
            'user_groups': user_groups,  
        }

        return render(request, 'base/dashboard.html', context)


class LandingPageView(TemplateView):
    template_name = "base/landing.html"