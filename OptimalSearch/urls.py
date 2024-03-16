from django.urls import path

from backend import views

urlpatterns = [
    path('api/writer/write_on_db/', views.write_on_db),
]
