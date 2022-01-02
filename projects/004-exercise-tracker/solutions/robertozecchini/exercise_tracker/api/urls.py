# api/urls.py

from django.urls import include, path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
users_list = views.UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    #path('', include(router.urls)),
    path('users/', users_list),
    path('users/:<slug:_id>/exercises/', views.CreateExercise),
    path('users/:<slug:_id>/logs/', views.ViewLog),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]