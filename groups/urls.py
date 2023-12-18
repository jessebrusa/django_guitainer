from django.urls import path
from .views import GroupPageView, AddUserView, RemoveUserView

urlpatterns = [
    path('group-page/<int:group_id>/', GroupPageView.as_view(), name='group-page'),

    path('add-user/<int:group_id>/', AddUserView.as_view(), name='add-user'),
    path('remove-user/<int:group_id>/<int:user_id>/', RemoveUserView.as_view(), name='remove-user'),
]
