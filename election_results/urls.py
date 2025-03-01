from django.urls import path
from . import views

app_name = 'election_results'

urlpatterns = [
    path('', views.polling_unit_result, name='polling_unit_result'),
    path('lga/', views.lga_result, name='lga_result'),
    path('store/', views.store_result, name='store_result'),
] 