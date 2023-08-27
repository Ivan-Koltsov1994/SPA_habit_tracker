from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users/', UsersListView.as_view(), name='users_list'),
    path('users/<int:pk>/', UsersDetailView.as_view(), name='users_detail'),
    path('user/create/', UsersCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/update/', UsersUpdateView.as_view(), name='user_update'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ]