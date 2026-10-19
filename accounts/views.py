"""Accounts views — Login, Register, Profile, Dashboard."""

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User, ContactMessage
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, ContactForm


class LoginView(TemplateView):
    """User login page."""
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()
        return context

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'خوش آمدید!')
                next_url = request.GET.get('next', reverse_lazy('accounts:dashboard'))
                return redirect(next_url)
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        return render(request, self.template_name, {'form': form})


class RegisterView(CreateView):
    """User registration page."""
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'ثبت‌نام با موفقیت انجام شد. لطفاً وارد شوید.')
        return redirect(self.success_url)


class DashboardView(LoginRequiredMixin, TemplateView):
    """User dashboard after login."""
    template_name = 'accounts/dashboard.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    """User profile edit page."""
    template_name = 'accounts/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'پروفایل با موفقیت بروزرسانی شد.')
        return super().form_valid(form)


class ContactView(CreateView):
    """Contact form page."""
    template_name = 'accounts/contact.html'
    model = ContactMessage
    form_class = ContactForm
    success_url = reverse_lazy('accounts:contact')

    def form_valid(self, form):
        messages.success(self.request, 'پیام شما با موفقیت ارسال شد.')
        return super().form_valid(form)


def logout_view(request):
    """Logout user."""
    logout(request)
    messages.info(request, 'با موفقیت خارج شدید.')
    return redirect('core:home')
