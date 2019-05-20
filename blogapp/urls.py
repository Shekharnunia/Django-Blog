from django.urls import path, include
from django.views.decorators.http import require_POST

from . import views


app_name = 'blogapp'
urlpatterns = [
    path('blog-list/', views.BlogListView.as_view(), name='list'),
    path('<slug:slug>/', views.DetailBlogView.as_view(), name='post'),
    # path('my_form/', require_POST(views.CommentFormView.as_view()), name='comment_form'),
    path('', views.index, name='index'),
]
