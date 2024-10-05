from django.urls import path
# Импортируем созданное нами представление
from .views import (
   PostList, PostDetail, PostSearch, PostDelete, PostCreate, PostUpdate, accept)
   # CategoryListView, subscribe)

urlpatterns = [

# path('', PostList.as_view(), name='post_list')
#    path('', .as_view(), name="profile"),

   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('create/', PostCreate.as_view(), name='post_create'),
   # # path('articles/create/', PostCreate.as_view(), name='article_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   # path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   # path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   # path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('accept/<int:pk>', accept, name='accept'),
]