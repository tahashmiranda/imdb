from django.urls import path
from django.conf.urls import url
from .views import MovieAPIView, MovieDetails
 
urlpatterns = [
 
    path('movies/', MovieAPIView.as_view()),
    path('movie/<int:id>/', MovieDetails.as_view()),
    path('movie/', MovieDetails.as_view())
 
 
]