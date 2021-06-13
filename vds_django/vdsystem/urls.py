from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vdsystem import views

router = DefaultRouter()

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]