from django.urls import path
from users.views import UserViewSet, UserHealthProfileViewSet, JournalEntryViewSet

urlpatterns = [
    # User Authentication
    path('auth/register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('auth/login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('auth/logout/', UserViewSet.as_view({'post': 'logout'}), name='user-logout'),
    path('auth/profile/', UserViewSet.as_view({'get': 'profile'}), name='user-profile'),
    path('auth/profile/update/', UserViewSet.as_view({'put': 'update_profile'}), name='user-update-profile'),
    path('auth/users/', UserViewSet.as_view({'get': 'users_list'}), name='users-list'),
    
    # Health Profile
    path('health-profile/', UserHealthProfileViewSet.as_view({'get': 'my_profile'}), name='health-profile'),
    path('health-profile/update/', UserHealthProfileViewSet.as_view({'put': 'update_profile'}), name='health-profile-update'),
    
    # Journal Entries
    path('journal/', JournalEntryViewSet.as_view({'get': 'entries'}), name='journal-list'),
    path('journal/add/', JournalEntryViewSet.as_view({'post': 'add_entry'}), name='journal-add'),
    path('journal/<uuid:entry_id>/edit/', JournalEntryViewSet.as_view({'put': 'edit_entry'}), name='journal-edit'),
    path('journal/<uuid:entry_id>/remove/', JournalEntryViewSet.as_view({'delete': 'remove_entry'}), name='journal-remove'),
]
