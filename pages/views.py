"""Pages views — About us, FAQ, Terms, and dynamic Static Pages."""

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, DetailView
from .models import FAQ, FAQCategory, Testimonial, TeamMember, StaticPage


class AboutUsView(TemplateView):
    template_name = 'pages/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = TeamMember.objects.filter(is_active=True)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)[:6]
        return context


class FAQView(TemplateView):
    template_name = 'pages/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FAQCategory.objects.prefetch_related('faqs').all()
        context['faqs'] = FAQ.objects.filter(is_active=True)
        return context


class StaticPageView(DetailView):
    model = StaticPage
    template_name = 'pages/static_page.html'
    context_object_name = 'page'
    slug_field = 'slug'
