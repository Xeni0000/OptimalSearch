from django.urls import path

from backend import views

urlpatterns = [
    path('api/writer/write_on_db/', views.write_on_db),
    path('api/finding_dependencies/tasks/', views.find_tasks_duplicate_dependence),
    path('api/main/role_list/', views.role_list),
    path('api/main/task_list/', views.task_list),
]
