from . import views
from django.urls import path

app_name = "FaceReco"

urlpatterns = [
    path("Processing/", views.processing, name="processing"),
    path("Reco/", views.reco, name="reco"),
    path("Rec/", views.rec, name="rec"),
    path("Analysis/", views.analysis, name="analysis"),
]
