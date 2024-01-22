from django.urls import path
from zira import views


# list of all urls 
urlpatterns = [
    path('gemini_text/', views.gemini_view, name="gemini-text"),
    path('gemini_image/', views.gemini_image_view, name="gemini-image"),
]
