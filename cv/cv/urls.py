from django.contrib import admin
from django.urls import path
from pdf import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accept, name="accept"),
    path('<int:id>/', views.resume, name="resume"),
    path('<int:id>/pdf/', views.generate_pdf, name="generate_pdf"),
    path('list/', views.list_profiles, name="list_profiles"),


]
