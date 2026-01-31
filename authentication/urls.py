from django.urls import path
from .views import SuperUserLoginView
from .product_views import ProductListCreateView, ProductDetailView, LatestProductsView, SetPrimaryImageView
from .user_views import UserListView, UserDetailView
from .about_views import AboutSectionView
from .sustainability_views import SustainabilityPillarListCreateView, SustainabilityPillarUpdateDeleteView
from .homestats_views import HomeStatsListCreateView, HomeStatsUpdateDeleteView
from .hero_views import HeroSectionView
from .tiktok_views import TikTokVideoListCreateView, TikTokVideoUpdateDeleteView
from .distributor_views import DistributorListCreateView, DistributorUpdateDeleteView
from .inquiry_views import InquiryListView, InquiryCreateView, InquiryDetailView
from .faq_views import FAQListCreateView, FAQUpdateDeleteView, PublicFAQListView
from .notice_views import NoticeListCreateView, NoticeUpdateDeleteView, PublicNoticeListView, PublicFeaturedNoticeView, NoticeArchiveStatsView
from .subscription_views import SubscriptionListView, SubscriptionCreateView, SubscriptionUpdateDeleteView
from .public_views import PublicDistributorListView
from .blog_views import (
    BlogListView, BlogDetailView, FeaturedBlogListView,
    BlogManagementListCreateView, BlogManagementDetailView
)
from .career_views import (
    CareerListView, CareerDetailView, JobApplicationCreateView,
    CareerManagementListCreateView, CareerManagementDetailView,
    JobApplicationManagementListView, JobApplicationManagementDetailView
)
from .order_views import OrderCreateView, OrderManagementListView, OrderManagementDetailView

urlpatterns = [
    path('login/', SuperUserLoginView.as_view(), name='superuser_login'),
    path('products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/set-primary-image/', SetPrimaryImageView.as_view(), name='set_primary_image'),
    path('products/latest/', LatestProductsView.as_view(), name='latest_products'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('about/', AboutSectionView.as_view(), name='about_section'),
    path('sustainability/', SustainabilityPillarListCreateView.as_view(), name='sustainability_list_create'),
    path('sustainability/<str:pillar_type>/', SustainabilityPillarUpdateDeleteView.as_view(), name='sustainability_update_delete'),
    path('homestats/', HomeStatsListCreateView.as_view(), name='homestats_list_create'),
    path('homestats/<str:stat_type>/', HomeStatsUpdateDeleteView.as_view(), name='homestats_update_delete'),
    path('hero/', HeroSectionView.as_view(), name='hero_section'),
    path('tiktok/', TikTokVideoListCreateView.as_view(), name='tiktok_list_create'),
    path('tiktok/<int:pk>/', TikTokVideoUpdateDeleteView.as_view(), name='tiktok_update_delete'),
    path('distributors/', DistributorListCreateView.as_view(), name='distributor_list_create'),
    path('distributors/<int:pk>/', DistributorUpdateDeleteView.as_view(), name='distributor_update_delete'),
    path('inquiries/', InquiryListView.as_view(), name='inquiry_list'),
    path('inquiries/<int:pk>/', InquiryDetailView.as_view(), name='inquiry_detail'),
    path('faqs/', FAQListCreateView.as_view(), name='faq_list_create'),
    path('faqs/<int:pk>/', FAQUpdateDeleteView.as_view(), name='faq_update_delete'),
    path('notices/', NoticeListCreateView.as_view(), name='notice_list_create'),
    path('notices/<int:pk>/', NoticeUpdateDeleteView.as_view(), name='notice_update_delete'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription_list'),
    path('subscriptions/<int:pk>/', SubscriptionUpdateDeleteView.as_view(), name='subscription_update_delete'),
    # Public endpoints
    path('public/distributors/', PublicDistributorListView.as_view(), name='public_distributors'),
    path('public/inquiries/', InquiryCreateView.as_view(), name='public_inquiry_create'),
    path('public/faqs/', PublicFAQListView.as_view(), name='public_faqs'),
    path('public/notices/', PublicNoticeListView.as_view(), name='public_notices'),
    path('public/notices/featured/', PublicFeaturedNoticeView.as_view(), name='public_featured_notices'),
    path('public/notices/archives/', NoticeArchiveStatsView.as_view(), name='notice_archives'),
    path('public/subscribe/', SubscriptionCreateView.as_view(), name='public_subscribe'),
    # Career endpoints
    path('careers/', CareerManagementListCreateView.as_view(), name='career_management'),
    path('careers/<int:pk>/', CareerManagementDetailView.as_view(), name='career_management_detail'),
    path('job-applications/', JobApplicationManagementListView.as_view(), name='job_application_management'),
    path('job-applications/<int:pk>/', JobApplicationManagementDetailView.as_view(), name='job_application_management_detail'),
    path('public/careers/', CareerListView.as_view(), name='public_careers'),
    path('public/careers/<int:pk>/', CareerDetailView.as_view(), name='public_career_detail'),
    path('public/job-applications/', JobApplicationCreateView.as_view(), name='public_job_application'),
    path('public/orders/', OrderCreateView.as_view(), name='public_order_create'),
    # Order management
    path('orders/', OrderManagementListView.as_view(), name='order_management'),
    path('orders/<int:pk>/', OrderManagementDetailView.as_view(), name='order_management_detail'),
    # Blog management
    path('blogs/', BlogManagementListCreateView.as_view(), name='blog_management'),
    path('blogs/<int:pk>/', BlogManagementDetailView.as_view(), name='blog_management_detail'),
    # Public blog endpoints
    path('public/blogs/', BlogListView.as_view(), name='public_blogs'),
    path('public/blogs/featured/', FeaturedBlogListView.as_view(), name='public_featured_blogs'),
    path('public/blogs/<slug:slug>/', BlogDetailView.as_view(), name='public_blog_detail'),
]