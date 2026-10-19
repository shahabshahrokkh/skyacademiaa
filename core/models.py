"""Core app models — Base abstract models for reuse across all apps."""

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    created_at = models.DateTimeField('تاریخ ایجاد', auto_now_add=True)
    updated_at = models.DateTimeField('تاریخ بروزرسانی', auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Abstract model with soft delete capability."""
    is_deleted = models.BooleanField('حذف شده', default=False)
    deleted_at = models.DateTimeField('تاریخ حذف', null=True, blank=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Abstract model for SEO fields."""
    meta_title = models.CharField('عنوان سئو', max_length=70, blank=True)
    meta_description = models.CharField('توضیحات سئو', max_length=160, blank=True)
    meta_keywords = models.CharField('کلمات کلیدی', max_length=255, blank=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Singleton model for global site configuration."""
    site_name = models.CharField('نام سایت', max_length=100, default='اسکای آکادمیا')
    site_description = models.TextField('توضیحات سایت', blank=True)
    logo = models.ImageField('لوگو', upload_to='site/', blank=True)
    favicon = models.ImageField('فاوآیکون', upload_to='site/', blank=True)
    phone = models.CharField('تلفن', max_length=20, blank=True)
    email = models.EmailField('ایمیل', blank=True)
    address = models.TextField('آدرس', blank=True)
    instagram = models.URLField('اینستاگرام', blank=True)
    telegram = models.URLField('تلگرام', blank=True)
    whatsapp = models.CharField('واتساپ', max_length=20, blank=True)
    linkedin = models.URLField('لینکدین', blank=True)
    footer_text = models.TextField('متن فوتر', blank=True)

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (Singleton)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
