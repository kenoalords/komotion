from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, JsonResponse
from django.views.generic import TemplateView, View, CreateView, DetailView, ListView, FormView, UpdateView
from academy.models import Slider, Course, CourseFile, Rank, Payment, Subscription
from academy.forms import CourseForm, CourseFileFormset, RankForm, SubscriptionForm
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import requests
import json

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

    def get_context_data(self, *args, **kwargs):
        print(kwargs)
        context = super().get_context_data(*args, **kwargs)
        context['files'] = CourseFile.objects.filter(course=self.object)
        return context

class VideoView(TemplateView):
    template_name = 'parts/tutorial/video.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                sub = Subscription.objects.get(user=request.user)
                if sub.end_date > date.today():
                    course = Course.objects.get(pk=kwargs['id'])
                    video = CourseFile.objects.get(pk=kwargs['video'])
                    coursefiles = CourseFile.objects.filter(course=course)
                    return render(request, template_name=self.template_name, context={ 'video': video, 'course': course, 'files': coursefiles })
                else:
                     return HttpResponseRedirect(reverse('academy:subscribe'))
            except Exception as e:
                print(e)
                return HttpResponseRedirect(reverse('academy:subscribe'))
        else:
            return HttpResponseRedirect(reverse('academy:subscribe'))

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

class DashboardView(TemplateView):
    template_name = 'user/dashboard.html'

class DashboardAdminCourses(TemplateView):
    template_name = 'user/courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

class AddCourse(TemplateView):
    template_name = 'user/add_course.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CourseForm(prefix='courseform')
        context['course_file_forms'] = CourseFileFormset(prefix='coursefileform')
        return context

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST, request.FILES, prefix='courseform')
        coursefiles = CourseFileFormset(request.POST, request.FILES, prefix='coursefileform')
        if form.is_valid() and coursefiles.is_valid():
            course = form.save()
            instances = coursefiles.save(commit=False)
            for instance in instances:
                instance.course = course
                instance.save()
                print('Saved!')
            messages.success(request, 'Course published successfully')
            return HttpResponseRedirect(reverse('academy:admin_courses'))
        else:
            return render(request, template_name=self.template_name, context={ 'form': form, 'course_file_forms': coursefiles } )

class EditCourse(UpdateView):
    template_name = 'user/edit_course.html'
    form_class = CourseForm
    model = Course
    slug_field = 'id'
    slug_url_kwarg = 'id'
    context_object_name = 'form'
    instance = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(id=self.kwargs['id'])
        context['course'] = course
        context['form'] = CourseForm(prefix='courseform', instance=course)
        context['course_file_forms'] = CourseFileFormset(prefix='coursefileform', instance=course)
        return context

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=self.kwargs['id'])
        form = CourseForm(request.POST, request.FILES, prefix='courseform', instance=course)
        coursefiles = CourseFileFormset(request.POST, request.FILES, prefix='coursefileform', instance=course)
        # print(coursefiles.errors)
        if form.is_valid() and coursefiles.is_valid():
            course = form.save()
            files = coursefiles.save()
            messages.success(request, '%s updated successfully' % course.title)
            return HttpResponseRedirect(reverse('academy:admin_courses'))
        else:
            return render(request, template_name=self.template_name, context={ 'form': form, 'course_file_forms': coursefiles, 'course': course } )

class DashboardAdminRank(TemplateView):
    template_name = 'user/ranks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ranks'] = Rank.objects.all()
        context['form'] = RankForm()
        return context

class DashboardAdminRankEdit(TemplateView):
    template_name = 'user/edit_rank.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rank = Rank.objects.get(id=self.kwargs['id'])
        context['form'] = RankForm(instance=rank)
        context['rank'] = rank
        return context

    def post(self, request, *args, **kwargs):
        rank = Rank.objects.get(id=self.kwargs['id'])
        form = RankForm(request.POST, request.FILES, instance=rank)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rank <strong>%s</strong> was updated successfully!' % rank.title)
            return HttpResponseRedirect(reverse('academy:admin_ranks'))
        else:
            context = {
                'form': RankForm(request.POST, request.FILES),
                'rank': rank
            }
            return render(request, template_name=self.template_name, context=context)

class SubscriptionView(TemplateView):
    template_name = "generic/subscribe.html"
    def get(self, request):
        return render( request, template_name = self.template_name )

    def post(self, request, *args, **kwargs):
        if request.POST['duration'] and request.POST['rank']:
            try:
                duration = int(request.POST['duration'])
                rank = int(request.POST['rank'])
                try:
                    get_rank = Rank.objects.get(id=rank)
                    url = reverse('academy:checkout') + '?rank='+str(rank)+'&duration='+str(duration)
                    return HttpResponseRedirect(url)
                except Exception as ex:
                    print(ex)
                    return render( request, template_name = self.template_name )
            except Exception as ex:
                # print(ex)
                return render( request, template_name = self.template_name )
        else:
            return render( request, template_name = self.template_name )

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('duration') is None and request.GET.get('rank') is None:
            return HttpResponseRedirect(reverse('academy:subscribe'))
        try:
            duration = int(request.GET['duration'])
            rank = int(request.GET['rank'])
            rank = Rank.objects.get(id=rank)
            cost = rank.cost * duration
            return render(request, template_name='generic/checkout.html', context={ 'rank': rank, 'cost': cost, 'duration': duration })
        except Exception as ex:
            print(ex)
            return HttpResponseRedirect(reverse('academy:subscribe'))

    def post(self, request, *args, **kwargs):
        if request.POST.get('duration') is None and request.POST.get('rank') is None:
            return HttpResponseRedirect(reverse('academy:subscribe'))

        duration = int(request.POST.get('duration'))
        rank = int(request.POST.get('rank'))
        rank = Rank.objects.get(id=rank)
        # goback_url = reverse('academy:checkout') + '?rank=' + str(rank.id) + '&duration=' + str(duration)
        goback_url = request.get_full_path()
        try:
            cost = int(rank.cost * duration * 100)
            try:
                payload = {
                    'email': self.request.user.email,
                    'amount': cost,
                    'metadata': {
                        'rank': rank.id,
                        'duration': duration
                    }
                }
                headers = {
                    'authorization': 'Bearer ' + settings.PAYSTACK_SECRET_KEY,
                    'content-type': 'application/json',
                    'cache-control': 'no-cache',
                }
                paystack = requests.post(settings.PAYSTACK_AUTH_URL, json=payload, headers=headers)
                response = json.loads(paystack.text)
                if response['status'] == True:
                    return HttpResponseRedirect(response['data']['authorization_url'])
                else:
                    return HttpResponseRedirect(goback_url)
            except Exception as e:
                print(e)
                return HttpResponseRedirect(goback_url)

        except Exception as ex:
            print(ex)
            return HttpResponseRedirect(goback_url)

class PaystackVerifyView(View):
    def get(self, request):
        if request.GET.get('reference'):
            ref = request.GET.get('reference')
            payload = {
                'authorization': 'Bearer ' + settings.PAYSTACK_SECRET_KEY,
                'accept': 'application/json',
                'cache-control': 'no-cache',
            }
            try:
                verify_tranx = requests.get(settings.PAYSTACK_VERIFY_TRANX_URL + ref, headers=payload)
                tranx = json.loads(verify_tranx.text)
                if tranx['status'] == True:
                    data = tranx['data']
                    amount = int(data['amount']) / 100
                    today = datetime.today()
                    duration = int(data['metadata']['duration'])
                    months = relativedelta(months=+duration)
                    end_date = today + months
                    payment, created = Payment.objects.get_or_create(user=request.user, amount=amount, tranx_ref=data['reference'])
                    if created == False:
                        return HttpResponseRedirect(reverse('academy:dashboard'))

                    rank = Rank.objects.get(id=int(data['metadata']['rank']))
                    try:
                        user_subscription = Subscription.objects.get(user=request.user)
                        user_subscription.end_date = end_date
                        user_subscription.is_active = True
                        user_subscription.rank = rank
                        user_subscription.save()
                        return render(request, template_name='generic/paystack_view.html')
                    except Subscription.DoesNotExist:
                        user_subcription = Subscription.objects.create(user=request.user, rank=rank, is_active=True, start_date=datetime.today(), end_date=end_date)
                        return render(request, template_name='generic/paystack_view.html')
                return render(request, template_name='generic/paystack_view.html')
            except Exception as ex:
                print(ex)
                return render(request, template_name='generic/paystack_view.html')
        return render(request, template_name='generic/paystack_view.html')

class AdminSubscriptionsView(TemplateView):
    template_name = 'user/admin_subscription.html'
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            return render(request, template_name=self.template_name, context={ 'subs': Subscription.objects.all() })
