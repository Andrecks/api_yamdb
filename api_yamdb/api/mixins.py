from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class GenreCategoryMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    pass
