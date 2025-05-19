from django.urls import path
from . import views

app_name = 'sagyodenpyo'

urlpatterns = [
    path('log/', views.log_work, name='log_work'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('loglist/', views.work_logs, name='work_logs'),
    path('list/', views.work_log_list, name='work_log_list'),
    path('edit/<int:pk>/', views.edit_work_log, name='edit_work_log'),
    path('totals/', views.log_totals, name='totals'),
    path('all-logs/', views.all_logs, name='all-logs'),
    path('all_logs_by_date/', views.all_work_logs_by_date, name='all_work_logs_by_date'),  # 新しいURL
    path('export_csv/', views.export_work_logs_csv, name='export_work_logs_csv'),  # CSVダウンロード用URL
    
]
