from django.shortcuts import render
from django.db.models import Count, Q
from django.views.generic import ListView, DetailView
from works.models import Art
import os
import folium


class ArtListView(ListView):
    model = Art
    template_name = "works/work_list.html"


class ArtListLocations(ListView):
    model = Art
    template_name = "works/work_locations.html"
    queryset = Art.objects


class ArtDetailView(DetailView):
    model = Art
    template_name = "works/work.html"
