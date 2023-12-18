from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Group, GroupSong, GroupUser


class GroupPageView(View):
    template_name = 'base/group.html'

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        group_songs = GroupSong.objects.filter(group=group)
        songs = [group_song.song for group_song in group_songs]
        current_user_group = GroupUser.objects.get(group=group, user=request.user)  
        is_current_user_admin = current_user_group.admin
        group_users = GroupUser.objects.filter(group=group).exclude(user=request.user)  
        users = [{'username': group_user.user.username, 'admin': group_user.admin} for group_user in group_users]
        context = {
            'name': group.name,
            'message': group.message,
            'is_current_user_admin': is_current_user_admin,
            'users': users,
            'songs': songs,
            'group_id': group.id, 
        }
        return render(request, self.template_name, context)
    

class AddUserView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username').lower()
        group_id = self.kwargs['group_id']

        try:
            user = User.objects.get(username=username)
            GroupUser.objects.create(user_id=user.id, group_id=group_id)
            return JsonResponse({'message': 'User added successfully.'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User does not exist.'}, status=400)
        


class RemoveUserView(View):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        group_id = self.kwargs['group_id']

        try:
            group_user = GroupUser.objects.get(user_id=user_id, group_id=group_id)
            group_user.delete()
            return JsonResponse({'message': 'User removed successfully.'}, status=200)
        except GroupUser.DoesNotExist:
            return JsonResponse({'message': 'User not found in this group.'}, status=400)