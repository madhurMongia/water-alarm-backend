from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tank', views.WaterTankView, basename='tank')
urlpatterns = [
    path('level/<tank_id>/', views.WaterLevelView.as_view(), name='level')
]
urlpatterns += router.urls
