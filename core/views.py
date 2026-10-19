"""Core views — Homepage and main landing pages."""

from django.shortcuts import render
from django.views.generic import TemplateView
from services.models import Service, ServiceCategory
from portfolio.models import Project
from blog.models import Post


class HomeView(TemplateView):
    """Homepage — hero, services, portfolio, testimonials, CTA."""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(
            is_active=True
        ).order_by('order')[:8]
        context['categories'] = ServiceCategory.objects.filter(
            is_active=True
        ).order_by('order')[:6]
        context['projects'] = Project.objects.filter(
            is_active=True, is_featured=True
        ).order_by('-created_at')[:6]
        context['latest_posts'] = Post.objects.filter(
            is_published=True
        ).order_by('-published_at')[:3]
        return context


class SearchView(TemplateView):
    """Search results page."""
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        if query:
            context['services'] = Service.objects.filter(
                title__icontains=query, is_active=True
            )
            context['posts'] = Post.objects.filter(
                title__icontains=query, is_published=True
            )
            context['projects'] = Project.objects.filter(
                title__icontains=query, is_active=True
            )
        return context
