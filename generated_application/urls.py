from django.urls import path
from <your application name> import views



urlpatterns = [
    path('project/', views.ProjectView.as_view(), name='project'),

]