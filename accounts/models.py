"""Accounts models — Custom User and Profile."""

from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel


class User(AbstractUser):
    """Custom user model with additional fields."""
    ROLE_CHOICES = [
        ('admin', 'مدیر'),
        ('staff', 'کارمند'),
        ('customer', 'مشتری'),
    ]

    phone = models.CharField('شماره تلفن', max_length=15, blank=True, unique=True, null=True)
    role = models.CharField('نقش', max_length=20, choices=ROLE_CHOICES, default='customer')
    avatar = models.ImageField('آواتار', upload_to='avatars/', blank=True)
    bio = models.TextField('درباره من', blank=True)
    city = models.CharField('شهر', max_length=100, blank=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.get_full_name() or self.username

    def get_display_name(self):
        return self.get_full_name() or self.username


class ContactMessage(TimeStampedModel):
    """Contact form submissions."""
    name = models.CharField('نام', max_length=100)
    email = models.EmailField('ایمیل')
    phone = models.CharField('تلفن', max_length=15, blank=True)
    subject = models.CharField('موضوع', max_length=200)
    message = models.TextField('پیام')
    is_read = models.BooleanField('خوانده شده', default=False)

    class Meta:
        verbose_name = 'پیام تماس'
        verbose_name_plural = 'پیام‌های تماس'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
