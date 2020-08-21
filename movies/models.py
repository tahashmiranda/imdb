
from django.db import models
from django_mysql.models import ListCharField   
 
# Create your models here.
 
class Genre(models.Model):
    genre = models.CharField(max_length=100)
    def __str__(self):
        return self.genre

class Movie(models.Model):
    popularity = models.FloatField()
    director = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    imdb_score = models.FloatField()
    name = models.CharField(max_length=100) 
    def __str__(self):
        return self.name

    # @classmethod
    # def create(cls, **kwargs):
    #     movie = cls.objects.create(
    #         popularity=kwargs['99popularity'],
    #         director=kwargs['director'],
    #         imdb_score=kwargs['imdb_score'],
    #         name=kwargs['name']
    #     )
    #     for genre_name in kwargs['genre']:
    #         genre, created = Genre.objects.get_or_create(genre=genre_name)
    #         movie.genre.add(genre)
    #     return movie