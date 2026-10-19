"""Pages models — About us, FAQ, Testimonials, Team, and Custom Pages."""

from django.db import models
from django.urls import reverse
from core.models import TimeStampedModel, SEOModel


class FAQCategory(models.Model):
    title = models.CharField('عنوان دسته‌بندی سوالات', max_length=100)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        verbose_name = 'دسته‌بندی سوالات'
        verbose_name_plural = 'دسته‌بندی‌های سوالات متداول'
        ordering = ['order']

    def __str__(self):
        return self.title


class FAQ(TimeStampedModel):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs', verbose_name='دسته‌بندی', null=True, blank=True)
    question = models.CharField('پرسش', max_length=255)
    answer = models.TextField('پاسخ')
    order = models.PositiveIntegerField('ترتیب', default=0)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'سوال متداول'
        verbose_name_plural = 'سوالات متداول (FAQ)'
        ordering = ['order', 'id']

    def __str__(self):
        return self.question


class Testimonial(TimeStampedModel):
    name = models.CharField('نام نظر دهنده', max_length=100)
    role = models.CharField('عنوان شغلی / زبان‌آموز', max_length=100, default='دانش‌پذیر دوره مکالمه')
    avatar = models.ImageField('تصویر کاربر', upload_to='testimonials/', blank=True)
    content = models.TextField('متن نظر')
    rating = models.PositiveSmallIntegerField('امتیاز (۱ تا ۵)', default=5)
    is_active = models.BooleanField('فعال', default=True)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        verbose_name = 'نظر مشتری / دانش‌پذیر'
        verbose_name_plural = 'نظرات مشتریان و دانش‌پذیران'
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.rating} ستاره)"


class TeamMember(models.Model):
    name = models.CharField('نام و نام خانوادگی', max_length=100)
    role = models.CharField('سمت / تخصص', max_length=100)
    avatar = models.ImageField('تصویر', upload_to='team/', blank=True)
    bio = models.TextField('بیوگرافی کوتاه', blank=True)
    order = models.PositiveIntegerField('ترتیب', default=0)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'عضو تیم / مدرس'
        verbose_name_plural = 'اعضای تیم و اساتید'
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} - {self.role}"


class StaticPage(TimeStampedModel, SEOModel):
    title = models.CharField('عنوان صفحه', max_length=150)
    slug = models.SlugField('اسلاگ (لاتین)', unique=True, allow_unicode=True)
    content = models.TextField('محتوای صفحه')
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'صفحه متنی'
        verbose_name_plural = 'صفحات متنی'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:static_page', kwargs={'slug': self.slug})
