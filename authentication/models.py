from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Baby Care', 'Baby Care'),
        ('Adult Care', 'Adult Care'),
        ('Feminine Care', 'Feminine Care'),
    ]
    
    BRAND_CHOICES = [
        ('HELEN HARPER', 'Helen Harper'),
        ('BABY CHARM', 'Baby Charm'),
    ]
    
    SIZE_CHOICES = [
        ('Newborn', 'Newborn'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True)
    pack_type = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    reviews_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.product.name} - Image"

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name='features', on_delete=models.CASCADE)
    feature = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.product.name} - {self.feature}"

class AboutSection(models.Model):
    title = models.CharField(max_length=200, default="Authorized Brand Seller and Distributor of Ontex Products")
    description = models.TextField(default="This page represents Neom, one of the authorized distributors of Ontex products in Nepal. Neom specializes in delivering high-quality baby care, feminine hygiene, and incontinence care products across all 7 provinces. As a trusted brand representative, Neom ensures hygienic and reliable product distribution throughout Nepal.")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"
    
    def __str__(self):
        return "About Section Content"
    
    def save(self, *args, **kwargs):
        # Ensure only one active about section exists
        if self.is_active:
            AboutSection.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class SustainabilityPillar(models.Model):
    PILLAR_TYPES = [
        ('planet', 'Better for Planet'),
        ('people', 'Better for People'),
        ('business', 'Better for Business'),
    ]
    
    pillar_type = models.CharField(max_length=20, choices=PILLAR_TYPES, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='sustainability/', blank=True, null=True)
    feature_title = models.CharField(max_length=200)
    feature_description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sustainability Pillar"
        verbose_name_plural = "Sustainability Pillars"
        ordering = ['pillar_type']

    def __str__(self):
        return f"{self.get_pillar_type_display()} - {self.title}"

class HomeStats(models.Model):
    STAT_TYPES = [
        ('products', 'Neom Products'),
        ('distributors', 'Neom Distributors'),
        ('experience', 'Our Experience'),
        ('brands', 'Partner Brands'),
    ]
    
    stat_type = models.CharField(max_length=20, choices=STAT_TYPES, unique=True)
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=10)
    icon = models.CharField(max_length=50, default='verified')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Home Statistic"
        verbose_name_plural = "Home Statistics"
        ordering = ['stat_type']

    def __str__(self):
        return f"{self.title} - {self.value}"

class HeroSection(models.Model):
    title = models.CharField(max_length=200, default="Authorized Brand Seller and Distributor of Ontex Products")
    subtitle = models.TextField(default="We sell premium Baby Charm and Helen Harper diapers - trusted hygiene solutions for families across Nepal.")
    image = models.ImageField(upload_to='hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section Content"
    
    def save(self, *args, **kwargs):
        # Ensure only one active hero section exists
        if self.is_active:
            HeroSection.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class TikTokVideo(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(help_text="TikTok video URL")
    thumbnail = models.ImageField(upload_to='tiktok_thumbnails/', help_text="Video thumbnail image")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "TikTok Video"
        verbose_name_plural = "TikTok Videos"
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

class Distributor(models.Model):
    PROVINCE_CHOICES = [
        ('Bagmati', 'Bagmati'),
        ('Koshi', 'Koshi'),
        ('Lumbini', 'Lumbini'),
        ('Gandaki', 'Gandaki'),
        ('Madhesh', 'Madhesh'),
        ('Karnali', 'Karnali'),
        ('Sudurpashchim', 'Sudurpashchim'),
    ]
    
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    map_link = models.URLField(blank=True, null=True, help_text="Google Maps link")
    distributor_type = models.CharField(max_length=50, default="Authorized Distributor")
    province = models.CharField(max_length=20, choices=PROVINCE_CHOICES, default='Bagmati')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Distributor"
        verbose_name_plural = "Distributors"
        ordering = ['name']

    def __str__(self):
        return self.name

class Inquiry(models.Model):
    SUBJECT_CHOICES = [
        ('General Distribution Inquiry', 'General Distribution Inquiry'),
        ('Order Tracking', 'Order Tracking'),
        ('Product Complaint', 'Product Complaint'),
        ('Branch Partnership', 'Branch Partnership'),
        ('Other', 'Other'),
    ]
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=100, choices=SUBJECT_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.subject}"

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.question

class Notice(models.Model):
    NOTICE_TYPES = [
        ('announcement', 'Announcement'),
        ('breaking', 'Breaking News'),
        ('policy', 'Policy Update'),
        ('maintenance', 'System Maintenance'),
        ('holiday', 'Holiday Notice'),
    ]
    
    title = models.CharField(max_length=300)
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    notice_type = models.CharField(max_length=20, choices=NOTICE_TYPES, default='announcement')
    image = models.ImageField(upload_to='notices/', blank=True, null=True)
    attachment = models.FileField(upload_to='notice_attachments/', blank=True, null=True, help_text="PDF or document attachment")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    is_featured = models.BooleanField(default=False, help_text="Show as breaking news")
    is_active = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notice"
        verbose_name_plural = "Notices"
        ordering = ['-published_date']

    def __str__(self):
        return self.title
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

class Subscription(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email

class Career(models.Model):
    JOB_TYPES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive Level'),
    ]
    
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default="Kathmandu, Nepal")
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full-time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='mid')
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., NPR 50,000 - 80,000")
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    requirements = models.TextField(help_text="Job requirements and qualifications")
    responsibilities = models.TextField(help_text="Key responsibilities")
    benefits = models.TextField(blank=True, help_text="Benefits and perks")
    application_deadline = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Career"
        verbose_name_plural = "Careers"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.department}"

class JobApplication(models.Model):
    APPLICATION_STATUS = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
    
    career = models.ForeignKey(Career, related_name='applications', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cv = models.FileField(upload_to='job_applications/', help_text="Upload your CV/Resume (PDF format preferred)")
    cover_letter = models.TextField(blank=True, help_text="Optional cover letter")
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending')
    notes = models.TextField(blank=True, help_text="Internal notes for HR")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        ordering = ['-applied_at']
        unique_together = ['career', 'email']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.full_name} - {self.career.title}"

class Order(models.Model):
    ORDER_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)
    delivery_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class Blog(models.Model):
    BLOG_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    excerpt = models.CharField(max_length=500, help_text="Brief description of the blog post")
    content = models.TextField(help_text="Full blog content with HTML formatting")
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.CharField(max_length=100, default="Neom Team")
    status = models.CharField(max_length=20, choices=BLOG_STATUS, default='draft')
    is_featured = models.BooleanField(default=False, help_text="Show as featured blog")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated read time in minutes")
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        
        if self.status == 'published' and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]