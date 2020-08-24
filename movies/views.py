from .models import Movie
from .serializers import MovieSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.views.generic.list import ListView
from rest_framework.pagination import PageNumberPagination
from movies.pagination import PaginationHandlerMixin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication,TokenAuthentication, BasicAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


def filter_results(results, request):
    """
    filters results based on the options passed in the query string
    """
    filter_genres = request.GET.get('genre')
    director = request.GET.get('director')
    sort_on = request.GET.get('sort_on')
    if filter_genres:
        filter_genres = filter_genres.split(",")
        for filter_genre in filter_genres:
            results = results.filter(
                Q(genre__genre__icontains=filter_genre)
            ).order_by('id')
    if director:
        results = results.filter(
                Q(director__icontains=director)
            ).order_by('id')
    if sort_on and sort_on == 'imdb_score_asc':
        results = results.filter(
            ).order_by('imdb_score')
    elif sort_on and sort_on == 'imdb_score_dsc':
        results = results.filter(
            ).order_by('-imdb_score')
    return results

class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class MovieAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    serializer_class = MovieSerializer

    def get(self, request):
        movies = Movie.objects.all()
        filtered_results = filter_results(movies, request)
        page = self.paginate_queryset(filtered_results)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,
                                                     many=True).data)
        else:
            serializer = self.serializer_class(filtered_results, many=True)
        return Response(serializer.data)


class MovieDetails(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated|ReadOnly]

    def get_object(self, id):
        try:
            return Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        movie = self.get_object(id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, id):
        movie = self.get_object(id)
        if type(movie) is Response:
            return movie
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        movie = self.get_object(id)
        if type(movie) is Response:
            return movie
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):    
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)