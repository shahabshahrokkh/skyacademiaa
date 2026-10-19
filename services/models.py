"""Services & Courses models — mirroring tikkaa.ir services & categories."""

from django.db import models
from django.urls import reverse
from core.models import TimeStampedModel, SEOModel


class ServiceCategory(TimeStampedModel):
    """Category of service/language (e.g. انگلیسی, آلمانی, دوره‌های سازمانی)."""
    title = models.CharField('عنوان دسته‌بندی', max_length=120)
    slug = models.SlugField('اسلاگ (لاتین)', unique=True, allow_unicode=True)
    icon = models.CharField('آیکون FontAwesome یا SVG', max_length=60, default='fa-graduation-cap', help_text='مانند fa-language یا fa-briefcase')
    short_desc = models.CharField('توضیح کوتاه', max_length=255, blank=True)
    color_accent = models.CharField('رنگ شاخص (Hex)', max_length=10, default='#372F7B')
    order = models.PositiveIntegerField('ترتیب نمایش', default=0)
    is_active = models.BooleanField('فعال', default=True)

    class Meta:
        verbose_name = 'دسته‌بندی خدمت / زبان'
        verbose_name_plural = 'دسته‌بندی‌های خدمات'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services:category_detail', kwargs={'slug': self.slug})


class Service(TimeStampedModel, SEOModel):
    """Service or Course offering (similar to Tikkaa's private classes, IELTS, etc.)."""
    LEVEL_CHOICES = [
        ('all', 'تمام سطوح'),
        ('beginner', 'مقدماتی'),
        ('intermediate', 'متوسط'),
        ('advanced', 'پیشرفته'),
    ]

    title = models.CharField('عنوان خدمت / دوره', max_length=200)
    slug = models.SlugField('اسلاگ (لاتین)', unique=True, allow_unicode=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services', verbose_name='دسته‌بندی')
    subtitle = models.CharField('زیرعنوان یا شعار کوتاه', max_length=255, blank=True)
    short_description = models.TextField('توضیح مختصر (برای کارت‌ها)', max_length=400)
    description = models.TextField('توضیحات کامل خدمت')
    cover_image = models.ImageField('تصویر کاور', upload_to='services/', blank=True)
    icon = models.CharField('کلاس آیکون', max_length=60, default='fa-book-open')
    
    # Pricing & Specs
    price = models.DecimalField('قیمت پایه (تومان)', max_digits=12, decimal_places=0, default=0, help_text='در صورت رایگان بودن 0 بگذارید')
    price_unit = models.CharField('واحد قیمت', max_length=50, default='هر جلسه / ساعت')
    duration = models.CharField('مدت زمان یا تعداد جلسات', max_length=100, default='۶۰ دقیقه هر جلسه')
    level = models.CharField('سطح دوره', max_length=20, choices=LEVEL_CHOICES, default='all')
    
    # Badges & Flags
    is_featured = models.BooleanField('نمایش در صفحه اصلی', default=True)
    is_popular = models.BooleanField('برچسب پرطرفدار', default=False)
    is_active = models.BooleanField('فعال', default=True)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        verbose_name = 'خدمت / دوره آموزشی'
        verbose_name_plural = 'خدمات و دوره‌ها'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services:service_detail', kwargs={'slug': self.slug})


class ServiceFeature(models.Model):
    """Key highlights of a service (e.g. کلاس آنلاین اختصاصی, تضمین یادگیری)."""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features', verbose_name='خدمت')
    title = models.CharField('ویژگی', max_length=150)
    order = models.PositiveIntegerField('ترتیب', default=0)

    class Meta:
        verbose_name = 'ویژگی خدمت'
        verbose_name_plural = 'ویژگی‌های خدمت'
        ordering = ['order']

    def __str__(self):
        return self.title


class ServiceLead(TimeStampedModel):
    """Consultation / registration request for a service."""
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads', verbose_name='خدمت انتخابی')
    full_name = models.CharField('نام و نام خانوادگی', max_length=100)
    phone = models.CharField('شماره تماس', max_length=15)
    description = models.TextField('توضیحات یا نیاز شما', blank=True)
    is_contacted = models.BooleanField('تماس گرفته شد؟', default=False)

    class Meta:
        verbose_name = 'درخواست مشاوره / رزرو'
        verbose_name_plural = 'درخواست‌های مشاوره و رزرو'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} ({self.phone})"
