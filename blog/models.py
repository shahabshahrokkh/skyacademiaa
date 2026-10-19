"""Blog models — articles, educational content, news."""

from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from core.models import TimeStampedModel, SEOModel


class BlogCategory(TimeStampedModel):
    title = models.CharField('عنوان دسته‌بندی', max_length=100)
    slug = models.SlugField('اسلاگ', unique=True, allow_unicode=True)

    class Meta:
        verbose_name = 'دسته‌بندی مقاله'
        verbose_name_plural = 'دسته‌بندی‌های وبلاگ'

    def __str__(self):
        return self.title


class Post(TimeStampedModel, SEOModel):
    title = models.CharField('عنوان مقاله', max_length=220)
    slug = models.SlugField('اسلاگ', unique=True, allow_unicode=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', verbose_name='نویسنده')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name='دسته‌بندی')
    cover_image = models.ImageField('تصویر شاخص', upload_to='blog/')
    summary = models.TextField('چکیده مقاله', max_length=350)
    content = models.TextField('متن کامل مقاله')
    reading_time = models.PositiveIntegerField('زمان تقریبی مطالعه (دقیقه)', default=5)
    views_count = models.PositiveIntegerField('تعداد بازدید', default=0)
    is_published = models.BooleanField('منتشر شده', default=True)
    published_at = models.DateTimeField('تاریخ انتشار', default=timezone.now)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات وبلاگ'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    name = models.CharField('نام شما', max_length=100)
    email = models.EmailField('ایمیل')
    message = models.TextField('دیدگاه شما')
    is_approved = models.BooleanField('تأیید شده برای نمایش', default=False)

    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه‌های مقالات'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} در {self.post.title}"
