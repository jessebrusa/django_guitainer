from django.urls import path
from .views import *

urlpatterns = [
    path('group-page/<int:group_id>/', GroupPageView.as_view(), name='group-page'),

    path('add-user/<int:group_id>/', AddUserView.as_view(), name='add-user'),
    
    path('make-admin/<int:group_id>/<int:user_id>/', MakeAdminView.as_view(), name='make-admin'),
    path('edit-message/<int:group_id>/', EditMessageView.as_view(), name='edit-message'),
    path('edit-group-name/<int:group_id>/', EditGroupNameView.as_view(), name='edit-group-name'),
    
    path('accept-user/<int:group_id>/', AcceptGroupView.as_view(), name='accept-user'),
    path('remove-user/<int:group_id>/<int:user_id>/', RemoveUserView.as_view(), name='remove-user'),
    path('remove-song-group/<int:group_id>/<int:song_id>/', RemoveSongGroupView.as_view(), name='remove-song-group'),
    path('delete-group/<int:group_id>/', DeleteGroupView.as_view(), name='delete-group'),

    path('create-group/', CreateGroupView.as_view(), name='create-group'),
    path('group-list/<int:song_id>', GroupListView.as_view(), name='group-list'),
    path('add-song-to-group/<int:group_id>/<int:song_id>/', AddSongGroupView.as_view(), name='add-song-to-group')
]
