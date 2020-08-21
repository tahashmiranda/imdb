from rest_framework import serializers
from .models import Movie, Genre
 
 

class MovieSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        for cur_genre in data['genre']:
            Genre.objects.get_or_create(genre=cur_genre)
        return super().to_internal_value(data)

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='genre',
        queryset = Genre.objects.all()
     )

    class Meta:
        model = Movie
        fields = '__all__'