from django.urls import path
from works import views

urlpatterns = [
    path("", views.ArtListView.as_view(), name="all-works"),
    path("<int:pk>/", views.ArtDetailView.as_view(), name="work"),
    path("locations/", views.ArtListLocations.as_view(), name="locations"),
]
