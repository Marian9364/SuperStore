from django.urls import path

from superstore.common.views import index, like_toy, copy_link_to_clipboard, comment_toy

urlpatterns = (
    path('', index, name='index'),
    path('like/<int:toy_id>/', like_toy, name='like'),
    path('share/<int:toy_id>/', copy_link_to_clipboard, name='share'),
    path('comment/<int:toy_id>/', comment_toy, name='comment'),
)