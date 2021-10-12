import django_filters as filters

from media.models import Categories, Genres, Titles


class TitlesFilter(filters.FilterSet):
    genre = filters.ModelChoiceFilter(
        field_name='genre__slug',
        to_field_name='slug',
        queryset=Genres.objects.all()
    )

    category = filters.ModelChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Categories.objects.all()
    )

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Titles
        fields = ('genre', 'category', 'year', 'name')