from django.urls import path
from . import views


app_name = 'myapp'

urlpatterns = [
    path('analysis/', views.analysis_view, name='analysis_view'),
    path('main/', views.main_view, name='main_view'),
    path('hlk/', views.hlk_view, name='hlk_view'),
    path('geo/', views.geo_view, name='geo_view'),
    path('personenbahnhoefe/', views.pb_view, name='pb_view'),
    path('personenbahnhoefe/<int:station_number>/', views.station_detail, name='pb_detail'),
]
