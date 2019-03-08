from django.urls import path
from importCsv.views import csv_import,csv_setting

urlpatterns = [
    path('setting/',csv_setting,name='setting-csv'),
    path('csv/',csv_import, name='import-csv'),
]