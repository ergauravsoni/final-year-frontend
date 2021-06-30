from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tower_blocks/', views.tower_blocks, name='tower_blocks'),
    path('bounce/', views.bounce, name='bounce'),
    path('kill_birds/', views.kill_birds, name='kill_birds'),
    path('snake/', views.snake, name='snake'),
]
