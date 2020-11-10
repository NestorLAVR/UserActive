from .  import views
from django.urls import path, include


urlpatterns = [
    path('fastprod', views.showhowmany, ),
    path('new_app1', views.show_app1, )
]