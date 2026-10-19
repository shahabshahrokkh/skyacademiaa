"""Blog views."""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import F
from .models import Post, BlogCategory, Comment


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True).select_related('author', 'category')
        cat_slug = self.request.GET.get('category')
        if cat_slug:
            qs = qs.filter(category__slug=cat_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment views safely
        Post.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['recent_posts'] = Post.objects.filter(is_published=True).exclude(pk=self.object.pk)[:4]
        return context


def submit_comment(request, slug):
    """Handle new comment submission."""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                message=message,
                is_approved=False
            )
            messages.success(request, 'دیدگاه شما با موفقیت ثبت شد و پس از بررسی منتشر خواهد شد.')
        else:
            messages.error(request, 'لطفاً تمامی فیلدها را تکمیل نمایید.')

    return redirect('blog:post_detail', slug=slug)
