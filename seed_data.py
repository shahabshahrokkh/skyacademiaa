"""Seed demo data script to populate the site with realistic Tikkaa-style content."""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import SiteSettings
from services.models import ServiceCategory, Service, ServiceFeature
from portfolio.models import ProjectCategory, Project
from blog.models import BlogCategory, Post
from pages.models import FAQCategory, FAQ, TeamMember, Testimonial

User = get_user_model()

def seed():
    print("[*] Seeding data...")

    # 1. Superuser
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin.first_name = 'مدیر'
        admin.last_name = 'سایت'
        admin.save()
        print("[+] Superuser created: admin / admin123")
    else:
        admin = User.objects.get(username='admin')

    # 2. Site Settings
    settings = SiteSettings.load()
    settings.site_name = 'اسکای آکادمیا'
    settings.site_description = 'سامانه هوشمند آموزش آنلاین و معرفی خدمات تخصصی با بالاترین کیفیت'
    settings.phone = '021-88997766'
    settings.email = 'info@sky-accademia.ir'
    settings.address = 'تهران، خیابان ولیعصر، برج فناوری و نوآوری، طبقه پنجم'
    settings.instagram = 'https://instagram.com/'
    settings.telegram = 'https://t.me/'
    settings.whatsapp = '989123456789'
    settings.footer_text = 'تمامی حقوق متعلق به اسکای آکادمیا است. پلتفرم تخصصی آموزش و مهارت‌آموزی آنلاین.'
    settings.save()
    print("[+] SiteSettings initialized.")

    # 3. Service Categories (Languages & Fields)
    cat_en, _ = ServiceCategory.objects.get_or_create(
        slug='english',
        defaults={'title': 'زبان انگلیسی', 'icon': 'fa-language', 'color_accent': '#372F7B', 'order': 1}
    )
    cat_de, _ = ServiceCategory.objects.get_or_create(
        slug='german',
        defaults={'title': 'زبان آلمانی', 'icon': 'fa-landmark', 'color_accent': '#008C95', 'order': 2}
    )
    cat_fr, _ = ServiceCategory.objects.get_or_create(
        slug='french',
        defaults={'title': 'زبان فرانسه', 'icon': 'fa-earth-europe', 'color_accent': '#FF7A00', 'order': 3}
    )
    cat_tr, _ = ServiceCategory.objects.get_or_create(
        slug='turkish',
        defaults={'title': 'ترکی استانبولی', 'icon': 'fa-passport', 'color_accent': '#E63946', 'order': 4}
    )
    cat_corp, _ = ServiceCategory.objects.get_or_create(
        slug='corporate',
        defaults={'title': 'پکیج‌های سازمانی', 'icon': 'fa-briefcase', 'color_accent': '#059669', 'order': 5}
    )

    # 4. Services
    s1, _ = Service.objects.get_or_create(
        slug='private-english-speaking',
        defaults={
            'title': 'کلاس خصوصی آنلاین مکالمه انگلیسی',
            'category': cat_en,
            'subtitle': 'تقویت مکالمه روان در ۳۰ جلسه با استاد اختصاصی',
            'short_description': 'تمرکز بر لهجه استاندارد، لیسنینگ و اصطلاحات روزمره و کاری بدون استرس با همراهی استاد برگزیده.',
            'description': 'این دوره به صورت کاملاً اختصاصی و متناسب با نیازهای کاری، تحصیلی یا مهاجرتی شما طراحی می‌شود. در هر جلسه ۶۰ دقیقه‌ای با تمرین‌های تعاملی، نقاط ضعف گفتاری شما شناسایی و برطرف خواهد شد.',
            'price': 280000,
            'price_unit': 'جلسه',
            'duration': '۶۰ دقیقه هر جلسه',
            'level': 'all',
            'is_featured': True,
            'is_popular': True,
            'order': 1
        }
    )
    ServiceFeature.objects.get_or_create(service=s1, title='برگزاری آنلاین در فضای اختصاصی')
    ServiceFeature.objects.get_or_create(service=s1, title='پشتیبانی رفع اشکال بین جلسات')
    ServiceFeature.objects.get_or_create(service=s1, title='تعیین سطح دقیق و برنامه منعطف')

    s2, _ = Service.objects.get_or_create(
        slug='ielts-preparation-intensive',
        defaults={
            'title': 'دوره فشرده آمادگی آزمون آیلتس (IELTS)',
            'category': cat_en,
            'subtitle': 'کسب نمره بالای ۷ در حداقل زمان ممکن',
            'short_description': 'تکنیک‌های حرفه‌ای Speaking و Writing همراه با تصحیح نامحدود تسک‌ها توسط اگزمینرهای مجرب.',
            'description': 'دوره جامع آیلتس شامل بررسی تخصصی ۴ مهارت، تحلیل آزمون‌های کمبریج، آموزش ساختارهای نمره‌آور و آزمون‌های ماک تستی با فیدبک تحلیلی.',
            'price': 390000,
            'price_unit': 'جلسه',
            'duration': '۹۰ دقیقه',
            'level': 'intermediate',
            'is_featured': True,
            'order': 2
        }
    )
    ServiceFeature.objects.get_or_create(service=s2, title='تصحیح منظم رایتینگ با فیدبک تحلیلی')
    ServiceFeature.objects.get_or_create(service=s2, title='ارائه منابع اختصاصی آزمون‌های اخیر')

    s3, _ = Service.objects.get_or_create(
        slug='german-a1-b2-migration',
        defaults={
            'title': 'دوره مکالمه و گرامر زبان آلمانی (ویژه مهاجرت)',
            'category': cat_de,
            'subtitle': 'آمادگی آزمون گوته و تلک از سطح مبتدی تا B2',
            'short_description': 'یادگیری اصولی زبان آلمانی جهت اخذ ویزای تحصیلی و کاری با اساتید مقیم آلمان.',
            'description': 'زبان آلمانی را به روش تعاملی و بر اساس کتاب‌های استاندارد Menschen و Sicher بیاموزید. این دوره شما را برای مصاحبه سفارت و آزمون‌های رسمی آماده می‌کند.',
            'price': 320000,
            'price_unit': 'جلسه',
            'duration': '۶۰ دقیقه',
            'level': 'beginner',
            'is_featured': True,
            'order': 3
        }
    )

    s4, _ = Service.objects.get_or_create(
        slug='corporate-training-packages',
        defaults={
            'title': 'پکیج آموزش زبان تخصصی شرکت‌ها و استارتاپ‌ها',
            'category': cat_corp,
            'subtitle': 'ارتقای مهارت پرسنل در مکاتبات تجاری و جلسات بین‌المللی',
            'short_description': 'برگزاری کلاس‌های گروهی و انفرادی برای سازمان‌ها همراه با گزارش پیشرفت ماهانه برای مدیران منابع انسانی.',
            'description': 'دوره ویژه شرکت‌های بازرگانی و IT جهت تسلط کارکنان بر ایمیل‌نگاری تجاری، پرزنت و شرکت در جلسات مذاکره بین‌المللی.',
            'price': 0,
            'price_unit': 'استعلام سفارشی',
            'duration': 'قرارداد سازمانی',
            'level': 'all',
            'is_featured': True,
            'order': 4
        }
    )
    print("[+] Services and categories populated.")

    # 5. Blog Posts
    b_cat, _ = BlogCategory.objects.get_or_create(slug='learning-tips', defaults={'title': 'نکات یادگیری زبان'})
    Post.objects.get_or_create(
        slug='how-to-speak-fluently-in-6-months',
        defaults={
            'title': 'چگونه در ۶ ماه به مکالمه روان انگلیسی برسیم؟',
            'author': admin,
            'category': b_cat,
            'reading_time': 6,
            'summary': 'راهنمای عملی یادگیری مکالمه بر اساس تکنیک غوطه‌وری و تمرین روزانه بدون نیاز به حفظ کردن گرامرهای پیچیده.',
            'content': 'رسیدن به روانی کلام نیازمند استمرار است، نه ساعت‌های طولانی در هفته. تکنیک سایه‌زنی (Shadowing)، پادکست‌های کوتاه روزانه و گفتگو با یک پارتنر یا استاد مجرب، سه رکن اساسی برای دستیابی به این هدف هستند.',
            'is_published': True
        }
    )
    Post.objects.get_or_create(
        slug='ielts-vs-toefl-full-comparison',
        defaults={
            'title': 'مقایسه جامع آزمون آیلتس و تافل در سال جدید',
            'author': admin,
            'category': b_cat,
            'reading_time': 8,
            'summary': 'بررسی تفاوت ساختار، هزینه‌ها، نمره‌دهی و پذیرش دانشگاه‌ها برای آزمون‌های IELTS و TOEFL.',
            'content': 'هر دو آزمون در سراسر دنیا معتبر هستند اما تفاوت‌های عمده‌ای در بخش اسپیکینگ و ریدینگ دارند. در این مقاله به شما کمک می‌کنیم بر اساس نقاط قوت خود، بهترین آزمون را انتخاب کنید.',
            'is_published': True
        }
    )
    print("[+] Blog posts populated.")

    # 6. Team & FAQs
    TeamMember.objects.get_or_create(
        name='دکتر کیانوش ناصری',
        defaults={'role': 'مدیر دپارتمان آیلتس و تافل', 'bio': 'دارای مدرک دکتری آموزش زبان انگلیسی و بیش از ۱۲ سال سابقه تدریس تخصصی.', 'order': 1}
    )
    TeamMember.objects.get_or_create(
        name='سارا محمدی',
        defaults={'role': 'مدرس ارشد زبان آلمانی', 'bio': 'دانش‌آموخته دانشگاه مونیخ و دارنده مدرک C2 گوته با ۸ سال سابقه تدریس.', 'order': 2}
    )

    FAQ.objects.get_or_create(
        question='نحوه ثبت‌نام و شروع جلسات به چه صورت است؟',
        defaults={'answer': 'پس از ثبت شماره تماس یا رزرو خدمت، مشاوران ما با شما تماس گرفته و بر اساس زمان‌های آزاد شما، جلسه آزمایشی یا کلاس را هماهنگ می‌کنند.'}
    )
    FAQ.objects.get_or_create(
        question='آیا گواهی پایان دوره اعطا می‌شود؟',
        defaults={'answer': 'بله، پس از پایان هر سطح آموزشی و موفقیت در آزمون جامع پایان دوره، مدرک رسمی دوزبانه قابل استعلام صادر می‌گردد.'}
    )
    print("[+] Team and FAQs populated.")
    print("[+] All demo data successfully seeded!")

if __name__ == '__main__':
    seed()
