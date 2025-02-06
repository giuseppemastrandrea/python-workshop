# pokemon/urls.py

from django.urls import path
from .views import PokemonSearch, PokemonDetailView

urlpatterns = [
    path("search/", PokemonSearch.as_view(), name="pokemon-search"),
    path("post/<int:pk>/", PokemonDetailView.as_view(), name="post_detail"),
]
