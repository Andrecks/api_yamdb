from media.models import Categories, Genres, Titles, Review, Comment
from users.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("me - недопустимый username")
        return data

class GetUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role',)

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        model = Genres


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'

# class CategoryField(serializers.SlugRelatedField):
#     def to_representation(self, value):
#         serializer = CategorySerializer(value)
#         return serializer.data


# class GenreField(serializers.SlugRelatedField):
#     def to_representation(self, value):
#         serializer = GenreSerializer(value)
#         return serializer.data

class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(), slug_field="slug"
    )
    description = serializers.CharField(required=False)
    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'text': {'required': True}}


class UserMeSerializer(serializers.ModelSerializer):

    role = serializers.CharField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role',)