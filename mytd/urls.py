"""
URL configuration for mytd project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from projects.views import (
    ProjectOverviewAPI, 
    ProjectDetailAPI, 
    ProjectDocumentCreateView, 
    ProjectFTESummaryView, 
    ProjectKPISummaryView
)

def home_view(request):
    return HttpResponse("Welcome to the MyTD API!")

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("", home_view, name="home"),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path("projects/", ProjectOverviewAPI.as_view(), name="project-overview"),
    path(
        "projects/<str:project_id>/",
        ProjectDetailAPI.as_view(),
        name="project-detail",
    ),
    #project documents
    path('projects/documents/add/', ProjectDocumentCreateView.as_view(), name='add-project-document'),
    #project KPI
    path('projects/kpis/add/', ProjectKPISummaryView.as_view(), name='kpi-create'),
    path('projects/kpis/<int:pk>/', ProjectKPISummaryView.as_view(), name='kpi-summary'),
    #project FTE Summary
    path('projects/fte-summary/', ProjectFTESummaryView.as_view(), name='fte-summary-create'),
    path('projects/fte-summary/<int:pk>/', ProjectFTESummaryView.as_view(), name='fte-summary'),
]
