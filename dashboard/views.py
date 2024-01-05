from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse

from django.shortcuts import render, redirect
from library.models import Song, SongUrl
from groups.models import Group, GroupUser
from django.contrib.auth.mixins import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        favorite_songs = Song.objects.select_related('songurl').filter(usersong__favorite=True, usersong__user=request.user)
        created_songs = Song.objects.select_related('songurl').filter(created=request.user)


        user_groups = GroupUser.objects.select_related('group').filter(user=request.user)
        group_ids = [group_user.group.id for group_user in user_groups]


        context = {
            'favorite_songs': favorite_songs,
            'created_songs': created_songs,
            'user_groups': user_groups,  
            'group_ids': group_ids,
        }

        return render(request, 'base/dashboard.html', context)


class LandingPageView(TemplateView):
    template_name = "base/landing.html"


class DeleteSongView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        song_id = kwargs.get('id')
        Song.objects.filter(id=song_id).delete()
        return JsonResponse({'status': 'success'})