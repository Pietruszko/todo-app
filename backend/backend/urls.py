from django.contrib import admin
from django.urls import path, include
from todos.views import TaskViewSet, RegisterView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.http import HttpResponse
from django.core.management import call_command
def run_migrations(request):
    call_command('migrate')
    return HttpResponse("Database migrations completed!")
temp_patterns = [
    path('secret-migrate/', run_migrations),  # Secret URL
]

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
]

urlpatterns += temp_patterns