from django.urls import path
from .views import (PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, add_subscribe, del_subscribe)
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', cache_page(60)(PostList.as_view()), name='post_list'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('add_subscribe/<int:pk>', add_subscribe, name='add_subscribe'),
   path('del_subscribe/<int:pk>', del_subscribe, name='del_subscribe'),
]

