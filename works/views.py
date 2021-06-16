from django.shortcuts import render
from django.db.models import Count, Q
from django.views.generic import ListView, DetailView
from works.models import Work, Iteration
import os
import folium


class WorkListView(ListView):
    model = Work
    template_name = "works/work_list.html"


class WorkListLocations(ListView):
    model = Work
    template_name = "works/work_locations.html"
    queryset = Work.objects.annotate(
        n_locs=Count('iterations', filter=Q(iterations__location__isnull=False))
    ).filter(n_locs__gt=0)

    def get_context_data(self, **kwargs):
        #shp_dir = os.path.join(os.getcwd(), 'media', 'shp')
        context = super().get_context_data(**kwargs)

        coordinates = []
        for work in self.queryset.prefetch_related('iterations'):
            iteration = work.iterations.filter(location__isnull=False).first()
            coordinates.append(iteration.location)

        avg_lat = sum(p[0] for p in coordinates) / len(coordinates)
        avg_lon = sum(p[1] for p in coordinates) / len(coordinates)


        figure = folium.Figure()
        m = folium.Map(
            location=(avg_lat, avg_lon),
            zoom_start=10,
            tiles='Stamen Terrain'
        )

        for point in coordinates:
            folium.Marker(
                location=(point[0], point[1]),
                icon=folium.Icon(color='red')
            ).add_to(m)


        m.add_to(figure)
        figure.render()
        context['map'] = figure
        #print(context)

        return context


class WorkDetailView(DetailView):
    model = Work
    template_name = "works/work.html"
