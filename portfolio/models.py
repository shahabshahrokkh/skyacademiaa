"""Portfolio & Projects models."""

from django.db import models
from django.urls import reverse
from core.models import TimeStampedModel, SEOModel


class ProjectCategory(TimeStampedModel):
    title = models.CharField('عنوان دسته‌بندی', max_length=100)
    slug = models.SlugField('اسلاگ', unique=True, allow_unicode=True)

    class Meta:
        verbose_name = 'دسته‌بندی نمونه کار'
        verbose_name_plural = 'دسته‌بندی‌های نمونه کار'

    def __str__(self):
        return self.title


class Project(TimeStampedModel, SEOModel):
    title = models.CharField('عنوان پروژه / نمونه کار', max_length=200)
    slug = models.SlugField('اسلاگ', unique=True, allow_unicode=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects', verbose_name='دسته‌بندی')
    client = models.CharField('کارفرما / دانش‌پذیر', max_length=120, blank=True)
    cover_image = models.ImageField('تصویر اصلی', upload_to='portfolio/')
    short_description = models.TextField('توضیح کوتاه', max_length=300)
    description = models.TextField('شرح جزئیات پروژه و نتایج')
    project_url = models.URLField('لینک پروژه', blank=True)
    is_featured = models.BooleanField('نمایش در صفحه اصلی', default=False)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'نمونه کار / پروژه'
        verbose_name_plural = 'نمونه کارها و پروژه‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})


class ProjectGallery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name='پروژه')
    image = models.ImageField('تصویر گالری', upload_to='portfolio/gallery/')
    caption = models.CharField('عنوان تصویر', max_length=150, blank=True)

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر پروژه'
