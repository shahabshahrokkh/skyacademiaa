# 🚀 پروژه اسکای آکادمیا (مشابه Tikkaa.ir)

پروژه با موفقیت بر پایه **Django 5 + Alpine.js + CSS Vanilla مدرن (RTL)** پیاده‌سازی شد. این معماری کاملاً سبک، مستقل از نود (No Node.js build required)، دارای SEO قوی به دلیل Server-Side Rendering و ۱۰۰٪ سازگار با سرورهای اشتراکی مثل **PythonAnywhere** است.

---

## 📂 ساختار ماژول‌ها و برنامه‌ها (Architecture)

```
Sky-Accademiaa/
├── manage.py
├── requirements.txt           # پکیج‌های سبک بدون نیاز به کامپایل سنگین
├── seed_data.py               # اسکریپت تولید خودکار داده‌های نمونه
├── db.sqlite3                 # دیتابیس آماده با داده‌های اولیه
├── .env                       # متغیرهای محیطی
│
├── config/                    # تنظیمات اصلی جنگو
│   ├── settings.py            # تنظیمات بومی‌سازی شده (Asia/Tehran, RTL, Custom User)
│   ├── urls.py                # روتینگ اصلی
│   └── wsgi.py                # وب‌سرور WSGI برای PythonAnywhere
│
├── core/                      # هسته اصلی
│   ├── models.py              # SiteSettings (تنظیمات سایت), TimeStampedModel, SEOModel
│   ├── context_processors.py  # تزریق SiteSettings به تمامی تمپلیت‌ها
│   ├── views.py               # HomeView (صفحه اصلی چندبخشی) و SearchView
│   └── urls.py
│
├── accounts/                  # ماژول کاربران و ارتباطات
│   ├── models.py              # User سفارشی (نقش‌ها، تلفن، آواتار)، ContactMessage
│   ├── forms.py               # فرم‌های ثبت‌نام، ورود، ویرایش پروفایل و تماس
│   ├── views.py               # لاگین، رجیستر، داشبورد کاربری و تماس
│   └── urls.py
│
├── services/                  # ماژول خدمات و دوره‌ها (مشابه کلاس‌های تیکا)
│   ├── models.py              # ServiceCategory (زبان‌ها/شاخه‌ها)، Service، ServiceFeature، ServiceLead
│   ├── views.py               # لیست خدمات با فیلتر دسته‌بندی، جزئیات خدمت، ثبت لید مشاوره
│   └── urls.py
│
├── portfolio/                 # ماژول نمونه‌کارها / افتخارات / سوابق
│   ├── models.py              # ProjectCategory، Project، ProjectGallery
│   ├── views.py
│   └── urls.py
│
├── blog/                      # وبلاگ و مقالات آموزشی
│   ├── models.py              # BlogCategory، Post (چکیده، زمان مطالعه، بازدید)، Comment
│   ├── views.py               # لیست مقالات، صفحه مقاله، ثبت دیدگاه
│   └── urls.py
│
├── pages/                     # صفحات ایستا و عمومی
│   ├── models.py              # FAQCategory، FAQ (آکاردئونی)، TeamMember، Testimonial، StaticPage
│   ├── views.py               # درباره ما، سوالات متداول، قوانین
│   └── urls.py
│
├── static/                    # فایل‌های استاتیک
│   ├── css/style.css          # استایل اختصاصی مدرن با پالت رنگی تیکا (#372F7B و #008C95)
│   ├── js/
│   └── images/
│
└── templates/                 # قالب‌های HTML تمیز و سمانتیک
    ├── base/base.html         # چیدمان والد با ساپورت Alpine.js، نوار پیام‌ها و مودال
    ├── includes/
    │   ├── header.html        # هدر واکنش‌گرا با جستجو، دکمه ورود و CTA
    │   └── footer.html        # فوتر ۴ ستونه مشابه تیکا
    ├── core/home.html         # استوری‌های هایلایت، هیرو، کارت‌های زبان، پلن‌ها، بنر لید
    ├── services/              # صفحات خدمات و جزئیات دوره
    ├── portfolio/             # لیست و جزئیات نمونه کارها
    ├── blog/                  # لیست و صفحه مقاله
    ├── pages/                 # درباره ما و FAQ
    └── accounts/              # ورود، ثبت‌نام، داشبورد و تماس
```

---

## 🔑 اطلاعات دسترسی پیش‌فرض (تست شده)

- **آدرس سایت محلی:** `http://127.0.0.1:8000/`
- **آدرس پنل مدیریت:** `http://127.0.0.1:8000/admin/`
- **نام کاربری ادمین:** `admin`
- **رمز عبور ادمین:** `admin123`

---

## 🌐 راهنمای دیپلوی روی PythonAnywhere (مرحله به مرحله)

### ۱. بارگذاری فایل‌ها در PythonAnywhere:
فایل‌های پوشه پروژه را می‌توانید از طریق Git یا آپلود فایل ZIP در مسیر زیر قرار دهید:
```bash
/home/yourusername/Sky-Accademiaa/
```

### ۲. ساخت Virtual Environment در کنسول Bash پایتون‌انی‌ور:
```bash
cd ~/Sky-Accademiaa
mkvirtualenv --python=/usr/bin/python3.11 sky-venv
pip install -r requirements.txt
python manage.py migrate
python seed_data.py
python manage.py collectstatic --noinput
```

### ۳. تنظیم بخش Web در کنترل‌پنل PythonAnywhere:
1. در تب **Web**، گزینه **Add a new web app** را بزنید و **Manual Configuration (Python 3.11)** را انتخاب کنید.
2. بخش‌های زیر را تکمیل نمایید:
   - **Source code:** `/home/yourusername/Sky-Accademiaa`
   - **Working directory:** `/home/yourusername/Sky-Accademiaa`
   - **Virtualenv:** `/home/yourusername/.virtualenvs/sky-venv`
3. در قسمت **Static files**:
   - URL: `/static/` &rarr; Directory: `/home/yourusername/Sky-Accademiaa/staticfiles/`
   - URL: `/media/` &rarr; Directory: `/home/yourusername/Sky-Accademiaa/media/`
4. روی فایل **WSGI configuration file** کلیک کرده و محتوای آن را به شکل زیر تنظیم کنید:
   ```python
   import os
   import sys

   path = '/home/yourusername/Sky-Accademiaa'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
5. دکمه سبز رنگ **Reload yourusername.pythonanywhere.com** را بزنید. سایت شما با سرعت بالا لود خواهد شد!
