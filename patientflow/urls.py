from django.contrib import admin
from django.urls import path, include
from patients.views import HomePageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home-page'),
    path('patients/', include('patients.urls', namespace='patients'))
]
