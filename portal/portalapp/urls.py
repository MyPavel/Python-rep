from django.urls import path
from .views import (ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, ResponseAdd,
                    ResponseList, ap_response, del_response)

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='post_delete'),
    path('<int:pk>/response', ResponseAdd.as_view(), name='response'),
    path('responses/', ResponseList.as_view(), name='responses'),
    path('responses/<int:pk>/accept', ap_response, name='accept_response'),
    path('responses/<int:pk>/delete', del_response, name='delete_response')
]
