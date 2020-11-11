from .  import views
from django.urls import path, include


urlpatterns = [
    path('fastprod', views.showhowmany, ),
    path('revenuegrid', views.show_app1, )
]