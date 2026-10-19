"""Services views — List, Detail, Category filter, and Consultation Request."""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.urls import reverse
from .models import Service, ServiceCategory, ServiceLead


class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        qs = Service.objects.filter(is_active=True).select_related('category')
        cat_slug = self.request.GET.get('category')
        if cat_slug:
            qs = qs.filter(category__slug=cat_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(is_active=True)
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_services'] = Service.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:3]
        return context


def request_consultation(request):
    """Handle instant consultation request form (HTMX or standard POST)."""
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        service_id = request.POST.get('service_id')
        description = request.POST.get('description', '').strip()

        if full_name and phone:
            service = Service.objects.filter(id=service_id).first() if service_id else None
            ServiceLead.objects.create(
                full_name=full_name,
                phone=phone,
                service=service,
                description=description
            )
            messages.success(request, 'درخواست مشاوره شما با موفقیت ثبت شد. مشاوران ما به زودی با شما تماس خواهند گرفت.')
        else:
            messages.error(request, 'لطفاً نام و شماره تماس خود را وارد نمایید.')

        next_url = request.POST.get('next', reverse('services:service_list'))
        return redirect(next_url)
    return redirect('services:service_list')
