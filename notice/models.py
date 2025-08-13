from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from web.models import Class, Department # Import existing models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class NoticeType(TimeStampModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Notice(TimeStampModel):
    title = models.CharField(max_length=255)
    short_description = models.TextField(help_text="A short description (max 2 lines) for the notice card.")
    file = models.FileField(
        upload_to='notices/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'])]
    )
    notice_type = models.ForeignKey(NoticeType, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Notices"
        ordering = ['-created_at']

    def __str__(self):
        return self.title