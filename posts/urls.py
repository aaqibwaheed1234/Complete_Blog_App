from django.urls import path
from .views import GetPosts,BaseView,BlogHomeView, CreatePost,PostDetail,UpdatePost, DeletePost, StoreComment, DeleteComment, LikePost, UserProfileView, SharePost, SearchView
urlpatterns = [
    path('',GetPosts.as_view(),name='posts'),
    path('home/',BlogHomeView.as_view(), name='home'),
    path('create-post/',CreatePost.as_view(), name='create-post'),
    path('post/<int:id>/',PostDetail.as_view(), name='post-details'),
    path('post/<int:pk>/delete/', DeletePost.as_view(),name='delete-post'),
    path('post/<int:pk>/update/', UpdatePost.as_view(), name='update-post'),

    path('store-comment/', StoreComment.as_view(), name='store-comment'),
    path('delete-comment/<int:pk>/',DeleteComment.as_view(), name='delete-comment'),
    path('like-post/<int:post_id>/',LikePost.as_view(), name='like-post'),
    path('share-post/<int:post_id>/', SharePost.as_view(), name='share-post'),
    path('search/', SearchView.as_view(), name='search'),

    path('user-profile/<int:post_id>/', UserProfileView.as_view(), name='user-profile'),
]

    