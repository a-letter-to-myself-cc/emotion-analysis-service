from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/emotions/', include('emotions.urls')),  # ✅ 모듈 라우팅
]

