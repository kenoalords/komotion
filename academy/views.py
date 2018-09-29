from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, JsonResponse
from django.views.generic import TemplateView, View, CreateView, DetailView, ListView, FormView, UpdateView
from academy.models import Slider, Course, CourseFile

# Create your views here.
class IndexView(TemplateView):
    template_name = 'generic/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.active.all()
        context['courses'] = Course.objects.all()[:5]
        return context

class TutorialView(DetailView):
    template_name = 'parts/tutorial/view.html'
    context_object_name = 'course'
    model = Course
    pk_url_kwarg = 'id'

class VideoView(TemplateView):
    template_name = 'parts/tutorial/video.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=kwargs['id'])
        context['video'] = CourseFile.objects.get(pk=kwargs['video'])
        return context

class BrowseTutorialView(TemplateView):
    template_name = 'parts/tutorial/browse.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            type = self.request.GET['type']
            browse = self.request.GET['browse']
            context['courses'] = self.fetch_tutorial(type, browse)
        except Exception as ex:
            context['courses'] = Course.objects.all()
        return context

    def fetch_tutorial(self, type, browse):
        if type == 'category':
            return Course.objects.filter(category__title__contains=browse)
        if type == 'rank':
            return Course.objects.filter(rank__title__contains=browse)
        if type == 'software':
            return Course.objects.filter(software__title__contains=browse)
