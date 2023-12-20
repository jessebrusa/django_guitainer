from django.urls import path
from .views import *

urlpatterns = [
    path('group-page/<int:group_id>/', GroupPageView.as_view(), name='group-page'),

    path('add-user/<int:group_id>/', AddUserView.as_view(), name='add-user'),
    path('remove-user/<int:group_id>/<int:user_id>/', RemoveUserView.as_view(), name='remove-user'),
    path('make-admin/<int:group_id>/<int:user_id>/', MakeAdminView.as_view(), name='make-admin'),
    path('edit-message/<int:group_id>/', EditMessageView.as_view(), name='edit-message'),
]
