from django.urls import path
from django.conf.urls import url
from . import views 
from .views import registration_view



urlpatterns = [
    

    path('register/',registration_view),
    path('api/login/', views.login),
    path('bookauthor/',views.bookauthor),
    path('comment/',views.get_comment),
    path('delcomment/<int:pk>/',views.delete_comment),


    
]