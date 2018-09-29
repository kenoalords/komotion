from django.urls import path, include
from academy.views import IndexView, TutorialView, VideoView, BrowseTutorialView
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings

app_name = 'academy'
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('how-it-works/', TemplateView.as_view(template_name="pages/how-it-works.html"), name="how_it_works"),
    path('tutorial/<int:id>', TutorialView.as_view(), name="view_tuts"),
    path('browse/', BrowseTutorialView.as_view(), name="browse_tuts"),
    path('tutorial/<int:id>/video/<int:video>/', VideoView.as_view(), name="view_video"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
