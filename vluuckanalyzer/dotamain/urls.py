from django.urls import path, re_path 
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', cache_page(1)(DotamainHome.as_view()), name = 'home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<int:post_id>/', ShowPost.as_view(), name='post'),
    path('category/<int:cat_id>/', cache_page(1)(DotamainCategory.as_view()), name='category')
    ]

