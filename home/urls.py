from django.urls import path
from .views import *

app_name = 'home'
urlpatterns = [

    path('',feed,name = 'feed'),
    path('new_post',new_post,name = 'new_post'),
    path('ajax/modify_like',modify_like,name='modify_like'),
    path('ajax/comment/<int:post_pk>/',comment_form,name='comment')
]
