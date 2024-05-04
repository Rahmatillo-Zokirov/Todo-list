from django.contrib import admin
from django.urls import path
from todoApp.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TasksView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logaout/', LogaoutView.as_view(), name='logaout'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='update'),
    path('register/', RegisterView.as_view(), name='register'),
]
