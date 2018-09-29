from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, reverse, redirect, render_to_response
from academy.auth_forms import CustomLoginForm, CustomUserCreationForm, CustomPasswordResetForm, CustomSetPasswordForm

class CustomLoginView(LoginView):
    model = User
    form_class = CustomLoginForm

class CustomRegisterationView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        next = ''
        # print(form.cleaned_data)
        if 'next' in self.request.GET:
            next = '?next=%s' % self.request.GET.get('next')
        try:
            email_check = User.objects.get(email__exact=email)
            return redirect(reverse("login") + next_link)
        except ObjectDoesNotExist:
            username = slugify(email)
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,last_name=last_name)
            if user:
                site = get_current_site(self.request)
                send_create_account_email.delay(email=email, first_name=first_name, site_name=site.name)
                auth_user = authenticate(username=username, password=password)
                if auth_user is not None:
                    login(self.request, auth_user)
                    return HttpResponseRedirect(self.request.GET.get('next') or '/')
                else:
                    return redirect(reverse("login"))

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('reset_password_done')
    email_template_name = 'email/password_reset_email.html'
    html_email_template_name = 'email/password_reset_email.html'
    subject_template_name = 'email/password_reset_email_subject.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    context_object_name = 'form'
    form_class = CustomSetPasswordForm

class CustomPasswordResetCompleteView(TemplateView):
    template_name = 'registration/password_reset_complete.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    form_class = CustomSetPasswordForm
