# web/urls.py

from django.urls import path
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('administration/', administration, name='administration'),
    
    # --- RENAMED & UNIVERSAL DOWNLOAD URL ---
    path('download/important-file/<int:pk>/', download_notice_file, name='download_notice_file'),

    # Other paths...
    path('students/', students, name='students'),
    path('filter/', filter_students, name='filter_students'),
    path('books/', books, name='books'),
    path('filter-books/', filter_books, name='filter_books'),
    path('syllabus/', syllabus, name='syllabus'),
    path('filter-syllabus/', filter_syllabus, name='filter_syllabus'),
    path('routine/', routine, name='routine'),
    path('filter-routines/', filter_routines, name='filter_routines'),
    path('download-routine/<int:pk>/', download_routine, name='download_routine'),
    path('download-book/<int:pk>/', download_book, name='download_book'),
    path('download-syllabus/<int:pk>/', download_syllabus, name='download_syllabus'),
    path('results/', result_list, name='result_list'),
    path('filter-results/', filter_results, name='filter_results'),
    path('download-result/<int:pk>/', download_result, name='download_result'),
    path('view-result-pdf/<int:pk>/', view_result_pdf, name='view_result_pdf'),
    path('admissions/', admission_list, name='admission_list'),
    path('filter-admissions/', filter_admissions, name='filter_admissions'),
    path('download-admission/<int:pk>/', download_admission, name='download_admission'),
    path('view-admission-pdf/<int:pk>/', view_admission_pdf, name='view_admission_pdf'),
    path('gallery/', gallery_list, name='gallery_list'),
    path('filter-gallery-images/', filter_gallery_images, name='filter_gallery_images'),
    path('filter-gallery-videos/', filter_gallery_videos, name='filter_gallery_videos'),
    path('information-service/', information_service, name='information_service'),
    path('filter-facilities/', filter_facilities, name='filter_facilities'),
    path('contact/', contact, name='contact'),
    path('contact/submit/', submit_contact_message, name='submit_contact_message'),
    
    # --- EVENTS AND NEWS ---
    path('events/', recent_events, name='recent_events'),
    path('events-view/', recent_events_view, name='recent_events_view'),
    path('samprotik-khobor/', samprotik_khobor, name='samprotik_khobor'),
    path('event-news-detail/<int:pk>/', event_news_detail, name='event_news_detail'),

    # --- API ENDPOINTS ---
    path('api/principal-message/', api_principal_message, name='api_principal_message'),

    path('footer/', footer_view, name='footer'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)