from django.urls import path
from .views import UpdateProfilePicture
from django.contrib.auth import views as auth_views
from .views import SignUpView, CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', UpdateProfilePicture.as_view(), name='profile'),
]
