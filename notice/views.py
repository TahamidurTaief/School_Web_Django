from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from .models import Notice, NoticeType
from web.models import Class, Department
import random

def notice_list(request):
    classes = Class.objects.all().order_by('numeric_value')
    departments = Department.objects.all()
    notice_types = NoticeType.objects.all()

    context = {
        'classes': classes,
        'departments': departments,
        'notice_types': notice_types,
    }
    return render(request, 'notice/notice_list.html', context)

def filter_notices(request):
    notice_type_slug = request.GET.get('type_slug')
    class_id = request.GET.get('class_id')
    dept_slug = request.GET.get('dept_slug')

    notices = Notice.objects.filter(is_active=True)

    if notice_type_slug:
        notices = notices.filter(notice_type__slug=notice_type_slug)
    if class_id and class_id.isdigit():
        notices = notices.filter(class_name_id=int(class_id))
    elif dept_slug:
        notices = notices.filter(department__slug=dept_slug)

    notices = notices.order_by('-created_at')

    notices_data = []
    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33FF', '#33FFFF', '#FFFF33'] # Example colors

    for notice in notices:
        notices_data.append({
            'id': notice.id,
            'title': notice.title,
            'short_description': notice.short_description,
            'file_url': notice.file.url,
            'download_url': f'/download-notice/{notice.id}/',
            'background_color': random.choice(colors),
            'notice_type': notice.notice_type.name,
            'class_name': notice.class_name.name if notice.class_name else '',
            'department': notice.department.name if notice.department else '',
        })

    return JsonResponse({'notices': notices_data})

def download_notice(request, pk):
    notice = Notice.objects.get(pk=pk)
    response = FileResponse(notice.file.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{notice.file.name}"'
    return response