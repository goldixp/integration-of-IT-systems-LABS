from django.contrib import admin
from django.urls import path, include  # Dodaj import 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('blog/', include('blog.urls')),
    path('pogogda/', include('external_data.urls')),
]