from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users import views

router = DefaultRouter()

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user-profiles')
router.register('api/auth', views.AuthViewSet, basename='auth')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]