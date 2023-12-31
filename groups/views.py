from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Group, GroupSong, GroupUser
from library.models import Song
from .forms import GroupForm
import json
from django.views.generic.edit import CreateView
from django.urls import reverse


class GroupPageView(LoginRequiredMixin, View):
    template_name = 'base/group.html'

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        group_songs = GroupSong.objects.filter(group=group)
        songs = [{'song': group_song.song, 'img_url': group_song.song.songurl.img} for group_song in group_songs]
        try:
            current_user_group = GroupUser.objects.get(group=group, user=request.user)  
            is_current_user_admin = current_user_group.admin
            group_users = GroupUser.objects.filter(group=group).exclude(user=request.user)  
            users = [{'username': group_user.user.username, 'admin': group_user.admin, 'user_id': group_user.user.id} for group_user in group_users]
            context = {
                'name': group.name,
                'message': group.message,
                'is_current_user_admin': is_current_user_admin,
                'users': users,
                'songs': songs,
                'group_id': group.id,
                'current_user_id': request.user.id,  
            }
            return render(request, self.template_name, context)
        except GroupUser.DoesNotExist:
            return redirect('/library/')
    

class AddUserView(View):
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username').lower()
        group_id = self.kwargs['group_id']
        make_admin = request.POST.get('make_admin_form') == 'on'

        try:
            user = User.objects.get(username=username)
            GroupUser.objects.create(user_id=user.id, group_id=group_id, admin=make_admin)
            return JsonResponse({'message': 'User added successfully.'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User does not exist.'}, status=400)
        


class RemoveUserView(View):
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        user_id = self.kwargs['user_id']
        
        print('GroupUser objects:', [(gu.user_id, gu.group_id) for gu in GroupUser.objects.all()])

        try:
            group_user = GroupUser.objects.get(user_id=user_id, group_id=group_id)
            group_user.delete()
            return JsonResponse({'status': 'success', 'message': 'User removed successfully.'}, status=200)

        except GroupUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found in this group.'}, status=400)
        

class MakeAdminView(View):
    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        group_id = self.kwargs['group_id']

        try:
            group_user = GroupUser.objects.get(user_id=user_id, group_id=group_id)
            group_user.admin = True
            group_user.save()
            return JsonResponse({'status': 'success', 'message': 'User made into admin.'}, status=200)

        except GroupUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found in this group.'}, status=400)
        

class EditMessageView(View):
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        data = json.loads(request.body)
        message = data.get('message')

        try:
            group = Group.objects.get(id=group_id)
            group.message = message
            group.save()
            return JsonResponse({'status': 'success'}, status=200)

        except GroupUser.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=400)


class RemoveSongGroupView(View):
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        song_id = self.kwargs['song_id']

        try:
            group_song = GroupSong.objects.get(song_id=song_id, group_id=group_id)
            group_song.delete()
            return JsonResponse({'status': 'success', 'message': 'User made into admin.'}, status=200)

        except GroupUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found in this group.'}, status=400)


class EditGroupNameView(View):
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']
        data = json.loads(request.body)
        group_name = data.get('group_name')

        try:
            group = Group.objects.get(id=group_id)
            group.name = group_name
            group.save()
            return JsonResponse({'status': 'success'}, status=200)

        except GroupUser.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=400)
        

class DeleteGroupView(View):
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs['group_id']

        try:
            group = Group.objects.get(id=group_id)
            group.delete()
            return JsonResponse({'status': 'success'}, status=200)

        except GroupUser.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=400)
        

class CreateGroupView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'base/group-form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        GroupUser.objects.create(user=self.request.user, group=self.object, admin=True, accept=True)
        return response
    
    def get_success_url(self):
        return reverse('group-page', args=[self.object.id])
    

class GroupListView(LoginRequiredMixin, ListView):
    model = GroupUser
    template_name = 'base/group-list.html'

    def get_queryset(self):
        song_id = self.kwargs.get('song_id')
        return GroupUser.objects.filter(user=self.request.user).exclude(group__groupsong__song=song_id)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_id'] = self.kwargs.get('song_id')
        return context
    

class AddSongGroupView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs.get('group_id')
        song_id = self.kwargs.get('song_id')
        group = Group.objects.get(id=group_id)
        song = Song.objects.get(id=song_id)
        GroupSong.objects.create(group=group, song=song)
        GroupUser.objects.get_or_create(user=request.user, group=group)
        return JsonResponse({'status': 'success'})
    
class AcceptGroupView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        group_id = self.kwargs.get('group_id')
        user_id = request.user.id
        group_user = GroupUser.objects.get(group_id=group_id, user_id=user_id)
        group_user.accept = True
        group_user.save()
        return JsonResponse({'status': 'success'})