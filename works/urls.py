from django.urls import path
from works import views

urlpatterns = [
    path("", views.WorkListView.as_view(), name="all-works"),
    path("<int:pk>/", views.WorkDetailView.as_view(), name="work"),
    path("locations/", views.WorkListLocations.as_view(), name="locations"),
]
