# web/context_processors.py

from .models import SchoolInfo
from notice.models import Notice

def school_info_processor(request):
    school_info = SchoolInfo.objects.first()
    latest_notices = Notice.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    return {
        'school_info': school_info,
        'latest_notices': latest_notices
    }