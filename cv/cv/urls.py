from django.contrib import admin
from django.urls import path
from pdf import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accept, name="accept"),
    path('<int:id>/', views.resume, name="resume"),
    path('<int:id>/pdf/', views.generate_pdf, name="generate_pdf"),
    path('list/', views.list_profiles, name="list_profiles"),
    path('share/email/<int:profile_id>/', views.share_cv_email, name='share_cv_email'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)