# web/models.py

from django.db import models
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class SchoolInfo(TimeStampModel):
    name = models.CharField(max_length=255, verbose_name="School Name")
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='school/', help_text="Upload the main logo for the navbar.")
    favicon = models.ImageField(upload_to='school/', blank=True, null=True, help_text="Upload a .ico or .png file for the browser tab icon.")
    established_year = models.CharField(max_length=4)
    description = models.TextField(null=True, blank=True, verbose_name="School Description")
    history = models.TextField(null=True, blank=True, verbose_name="School History")
    vision = models.TextField(null=True, blank=True, verbose_name="School Vision")
    mission = models.TextField(null=True, blank=True, verbose_name="School Mission")
    reg_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Registration Number")
    facebook_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Facebook URL")
    instagram_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="Instagram URL")
    youtube_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="YouTube URL")
    linkedin_url = models.URLField(max_length=255, blank=True, null=True, verbose_name="LinkedIn URL")

    class Meta:
        verbose_name_plural = 'স্কুলের তথ্য'

    def __str__(self):
        return self.name


class Department(TimeStampModel):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    male_student = models.IntegerField(default=0, verbose_name="Male Students (Manual)")
    female_student = models.IntegerField(default=0, verbose_name="Female Students (Manual)")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'বিভাগের তথ্য'

    def __str__(self):
        return self.name
    
    @property
    def total_students(self):
        return self.male_student + self.female_student



class Class(TimeStampModel):
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    numeric_value = models.IntegerField(unique=True)
    description = models.TextField(blank=True)
    male_student = models.IntegerField(default=0, verbose_name="Male Students (Manual)")
    female_student = models.IntegerField(default=0, verbose_name="Female Students (Manual)")
    show_students_publicly = models.BooleanField(default=True, help_text="Display student list publicly for this class.")

    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['numeric_value']

    class Meta:
        verbose_name_plural = 'ক্লাসের তথ্য'

    def __str__(self):
        return self.name
    
    @property
    def total_students(self):
        return self.male_student + self.female_student
    

# class Teacher(TimeStampModel):
#     CATEGORY_CHOICES = [
#         ('special_officer', 'Special Officer'),
#         ('teacher', 'Teacher'),
#         ('management_board', 'Management Board'),
#         ('administration', 'Administration'),
#         ('kormochari', 'Kormochari Brindo'),
#     ]
#     category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default='teacher', verbose_name='Category')
#     name = models.CharField(max_length=100)
#     position = models.CharField(max_length=100)
#     photo = models.ImageField(upload_to='teachers/')
#     education = models.CharField(max_length=200, blank=True)
#     specialization = models.CharField(max_length=200, blank=True)
#     experience = models.TextField(blank=True)
#     facebook = models.URLField(blank=True)
#     twitter = models.URLField(blank=True)
#     linkedin = models.URLField(blank=True)
#     email = models.EmailField(blank=True)
#     phone = models.CharField(max_length=20, blank=True)
#     is_special_officer = models.BooleanField(default=False)

#     class Meta:
#         verbose_name_plural = 'শিক্ষকদের তথ্য'

#     def __str__(self):
#         return f"{self.name} - {self.position}"

    


class FacultyMember(TimeStampModel):
    CATEGORY_CHOICES = [
        ('teacher', 'Teacher'),
        ('management', 'Management'),
        ('administration', 'Administration'),
        ('staff', 'Staff (Kormochari)'),
    ]
    
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default='teacher', verbose_name='Category')
    name = models.CharField(max_length=200, verbose_name='Name')
    position = models.CharField(max_length=200, verbose_name='Position')
    department = models.CharField(max_length=200, blank=True, verbose_name='Department')
    education = models.CharField(max_length=200, blank=True, verbose_name='Education')
    experience = models.CharField(max_length=100, blank=True, help_text="Years of experience", verbose_name='Experience')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Phone')
    photo = models.ImageField(upload_to='faculty_photos/', blank=True, verbose_name='Photo')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    order = models.IntegerField(default=0, verbose_name='Order')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Faculty Member'
        verbose_name_plural = 'কর্মকর্তাদের তথ্য'

    def __str__(self):
        return f"{self.name} - {self.position}"




class Student(TimeStampModel):
    GENDER_CHOICES = (
        ('Male', 'ছাত্র'),
        ('Female', 'ছাত্রী'),
        ('Other', 'অন্যান্য'),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male', verbose_name="লিঙ্গ")
    roll_number = models.CharField(max_length=20)
    registration_number = models.CharField(max_length=20)
    class_name = models.ForeignKey(
        Class, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )
    photo = models.ImageField(upload_to='students/', blank=True)
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=20)
    address = models.TextField()

    class Meta:
        verbose_name_plural = 'শিক্ষার্থীদের তথ্য'

    def __str__(self):
        return f"{self.name}"
    


class Notice(TimeStampModel):
    NOTICE_TYPES = (
        ('notice', 'Notice'),
        ('result', 'Result'),
        ('admission', 'Admission'),
        ('routine', 'Routine')
    )

    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=NOTICE_TYPES)
    date = models.DateField()
    file = models.FileField(
        upload_to='notices/',
        validators=[FileExtensionValidator(['pdf'])]
    )
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = 'নোটিশ'

    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"


class Slider(models.Model):
    image = models.ImageField(upload_to='sliders/')
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'স্লাইডার'
        ordering = ['-created_at']

    def __str__(self):
        return self.title if self.title else f"Slider {self.id}"


        

class PrincipalRole(TimeStampModel):
    name = models.CharField(max_length=100, verbose_name='Role Name')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'গুরুত্বপূর্ণ পদ'
        verbose_name_plural = 'গুরুত্বপূর্ণ পদ সমূহ'

    def __str__(self):
        return self.name
    




class ImportantLink(TimeStampModel):
    title = models.CharField(max_length=200, verbose_name='শিরোনাম')
    url = models.URLField(verbose_name='লিঙ্ক')
    icon = models.CharField(max_length=50, blank=True, verbose_name='আইকন (FontAwesome)')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'গুরুত্বপূর্ণ লিঙ্ক'
        verbose_name_plural = 'গুরুত্বপূর্ণ লিঙ্কসমূহ'

    def __str__(self):
        return self.title

class RoutineType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'রুটিনের ধারা'
        verbose_name_plural = 'রুটিনের ধারা সমূহ'

    def __str__(self):
        return self.name

class Routine(models.Model):
    ROUTINE_CATEGORIES = (
        ('class', 'Class Routine'),
        ('exam', 'Exam Routine'),
    )

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=ROUTINE_CATEGORIES)
    routine_type = models.ForeignKey(RoutineType, on_delete=models.SET_NULL, null=True, blank=True)
    class_name = models.ForeignKey(
        Class,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='routines'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='routines'
    )
    file = models.FileField(upload_to='routines/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'রুটিন'
        verbose_name_plural = 'রুটিন সমূহ'

    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    class_name = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='books/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'বই'
        verbose_name_plural = 'বইসমূহ'

    def __str__(self):
        return self.title

class Syllabus(models.Model):
    title = models.CharField(max_length=200, verbose_name='পাঠ্যক্রমের শিরোনাম')
    class_name = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='শ্রেণি')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='বিভাগ')
    file = models.FileField(upload_to='syllabus/', blank=True, verbose_name='পাঠ্যক্রম ফাইল')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'পাঠ্যক্রম'
        verbose_name_plural = 'পাঠ্যক্রম সমূহ'

    def __str__(self):
        return self.title

class Result(TimeStampModel):
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='results/',
        validators=[FileExtensionValidator(['pdf'])]
    )
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "ফলাফল"
        verbose_name_plural = "ফলাফলসমূহ"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Admission(TimeStampModel):
    title = models.CharField(max_length=255, verbose_name='ভর্তির শিরোনাম')
    file = models.FileField(
        upload_to='admissions/',
        validators=[FileExtensionValidator(['pdf'])],
        verbose_name='ভর্তির ফাইল'
    )
    class_name = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='শ্রেণি')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='বিভাগ')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')

    class Meta:
        verbose_name = 'ভর্তি'
        verbose_name_plural = "ভর্তিসমূহ"
        ordering = ['-created_at']

    def __str__(self):
        return self.title



class Gallery(TimeStampModel):
    CATEGORIES = (
        ('school', 'School'),
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField(blank=True)
    is_slider = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'গ্যালারী'

    def __str__(self):
        return self.title


class Video(TimeStampModel):
    title = models.CharField(max_length=255)
    youtube_url = models.URLField(max_length=500, blank=True, null=True, help_text="Full YouTube URL (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
    youtube_id = models.CharField(max_length=50, blank=True, help_text="The YouTube video ID (e.g., dQw4w9WgXcQ) - will be auto-extracted from URL")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True)

    class Meta:
        verbose_name_plural = "ভিডিও"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def extract_youtube_id(self, url):
        """Extract YouTube video ID from various YouTube URL formats"""
        import re
        
        if not url:
            return ""
            
        # YouTube URL patterns
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
            r'youtu\.be/([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # If no pattern matches, assume it's already a video ID
        if len(url) == 11 and re.match(r'^[a-zA-Z0-9_-]+$', url):
            return url
            
        return ""

    def save(self, *args, **kwargs):
        """Auto-extract YouTube ID from URL before saving"""
        if self.youtube_url and not self.youtube_id:
            self.youtube_id = self.extract_youtube_id(self.youtube_url)
        elif not self.youtube_url and self.youtube_id:
            # If only ID is provided, construct the URL
            self.youtube_url = f"https://www.youtube.com/watch?v={self.youtube_id}"
        super().save(*args, **kwargs)

    @property
    def embed_url(self):
        """Get the embeddable YouTube URL"""
        if self.youtube_id:
            return f"https://www.youtube.com/embed/{self.youtube_id}?rel=0&modestbranding=1"
        return ""

    @property
    def thumbnail_url(self):
        """Get the YouTube thumbnail URL"""
        if self.youtube_id:
            return f"https://img.youtube.com/vi/{self.youtube_id}/maxresdefault.jpg"
        return ""

# class InformationService(TimeStampModel):
#     """Main model for Information Service Center"""
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         verbose_name_plural = "Information Service"

#     def __str__(self):
#         return self.title

# class InformationSlider(TimeStampModel):
#     """Sliding photo gallery for information service"""
#     title = models.CharField(max_length=200)
#     image = models.ImageField(upload_to='information_slider/')
#     description = models.TextField(blank=True)
#     order = models.IntegerField(default=0)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         ordering = ['order', '-created_at']
#         verbose_name_plural = "তথ্যসহ স্লাইডার"

#     def __str__(self):
#         return self.title








# New model for dynamic facility types (now after TimeStampModel)
class FacilityType(TimeStampModel):
    name = models.CharField(max_length=100, unique=True, verbose_name='Facility Type Name')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'সুযোগ সুবিধা'
        verbose_name_plural = 'সুযোগ সুবিধাসমূহ'

    def __str__(self):
        return self.name


        

class FacilityInfo(TimeStampModel):
    """School facilities information"""
    facility_type = models.ForeignKey('FacilityType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Facility Type', related_name='facilities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    count = models.IntegerField(default=0, help_text="Number/Count for this facility")
    unit = models.CharField(max_length=20, blank=True, help_text="Unit (e.g., 'টি', 'জন', 'খানা')")
    image = models.ImageField(upload_to='facilities/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "সুযোগ সুবিধার তথ্য"

    def __str__(self):
        return f"{self.facility_type} - {self.title}"

class FacultyInfo(TimeStampModel):
    """Faculty information for information service"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True)
    education = models.CharField(max_length=200, blank=True)
    experience = models.CharField(max_length=100, blank=True, help_text="Years of experience")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='faculty/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "কমিটির তথ্য"

    def __str__(self):
        return f"{self.name} - {self.position}"

class ContactInfo(TimeStampModel):
    """Public contact information for the school"""
    title = models.CharField(max_length=200, verbose_name='শিরোনাম')
    address = models.TextField(verbose_name='ঠিকানা')
    phone = models.CharField(max_length=30, verbose_name='ফোন নম্বর')
    email = models.EmailField(verbose_name='ইমেইল')
    map_embed = models.TextField(blank=True, verbose_name='গুগল ম্যাপ এম্বেড কোড', help_text='গুগল ম্যাপ এম্বেড কোড (ঐচ্ছিক)')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')

    class Meta:
        verbose_name = 'যোগাযোগের তথ্য'
        verbose_name_plural = 'যোগাযোগের তথ্যসমূহ'

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    """Messages submitted via the public contact form"""
    name = models.CharField(max_length=100, verbose_name='নাম')
    phone = models.CharField(max_length=30, verbose_name='ফোন নম্বর')
    title = models.CharField(max_length=200, verbose_name='বার্তার শিরোনাম')
    message = models.TextField(verbose_name='বার্তার বিবরণ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='পাঠানোর সময়')
    is_read = models.BooleanField(default=False, verbose_name='পড়া হয়েছে')

    class Meta:
        verbose_name = 'যোগাযোগ বার্তা'
        verbose_name_plural = 'যোগাযোগ বার্তাসমূহ'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.name} ({self.phone})"

class News(TimeStampModel):
    """News items for the home page"""
    title = models.CharField(max_length=200, verbose_name='শিরোনাম')
    description = models.TextField(blank=True, verbose_name='বিবরণ')
    link = models.URLField(verbose_name='লিঙ্ক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'সংবাদ'
        verbose_name_plural = 'সংবাদসমূহ'

    def __str__(self):
        return self.title

class NewsLink(TimeStampModel):
    """News and Links section for home page"""
    title = models.CharField(max_length=200, verbose_name='শিরোনাম', default='সংবাদ/প্রয়োজনীয় লিংক')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')

    class Meta:
        verbose_name = 'সংবাদ ও লিঙ্ক বিভাগ'
        verbose_name_plural = 'সংবাদ ও লিঙ্ক বিভাগসমূহ'

    def __str__(self):
        return self.title

# About Page Models
class AboutPage(TimeStampModel):
    """Main about page configuration"""
    title = models.CharField(max_length=200, default='আমাদের সম্পর্কে (About Us)', verbose_name='পৃষ্ঠার শিরোনাম')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')

    class Meta:
        verbose_name = 'আমাদের সম্পর্কে পৃষ্ঠা'
        verbose_name_plural = 'আমাদের সম্পর্কে পৃষ্ঠা'

    def __str__(self):
        return self.title

class SchoolHistory(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='history/', blank=True, null=True)

    class Meta:
        verbose_name = 'প্রতিষ্ঠানের ইতিহাস'
        verbose_name_plural = 'প্রতিষ্ঠানের ইতিহাস'

    def __str__(self):
        return self.title

class SchoolBriefInfo(TimeStampModel):
    """School brief information with statistics"""
    title = models.CharField(max_length=200, default='সংক্ষিপ্ত তথ্য', verbose_name='শিরোনাম')
    description = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    teachers_count = models.CharField(max_length=20, default='৫০+', verbose_name='শিক্ষক-শিক্ষিকার সংখ্যা')
    departments_count = models.CharField(max_length=20, default='৫', verbose_name='বিভাগের সংখ্যা')
    classrooms_count = models.CharField(max_length=20, default='৩০+', verbose_name='ক্লাসরুমের সংখ্যা')
    students_count = models.CharField(max_length=20, default='১০০০+', verbose_name='শিক্ষার্থীর সংখ্যা')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'সংক্ষিপ্ত তথ্য'
        verbose_name_plural = 'সংক্ষিপ্ত তথ্য'

    def __str__(self):
        return self.title

class AboutMessage(TimeStampModel):
    """Message from officials for about page"""
    title = models.CharField(max_length=200, default='অধ্যক্ষের বাণী', verbose_name='শিরোনাম')
    name = models.CharField(max_length=100, verbose_name='নাম')
    position = models.CharField(max_length=100, verbose_name='পদবী/পদ')
    message = models.TextField(verbose_name='বার্তা')
    photo = models.ImageField(upload_to='about/message/', blank=True, verbose_name='ছবি')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    serial_no = models.IntegerField(default=0, verbose_name='ক্রমিক নম্বর')
    show_on_home_page = models.BooleanField(
        default=False,
        verbose_name="হোম পেজে দেখান",
        help_text="হোম পেজে দেখানোর জন্য টিক দিন।"
    )

    # def save(self, *args, **kwargs):
    #     # If this message is being set to show on the home page
    #     if self.show_on_home_page:
    #         # Unset any other message that might be currently featured
    #         AboutMessage.objects.filter(show_on_home_page=True).exclude(pk=self.pk).update(show_on_home_page=False)
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ['serial_no', '-created_at']
        verbose_name = 'বার্তা (আমাদের সম্পর্কে)'
        verbose_name_plural = 'বার্তাসমূহ (আমাদের সম্পর্কে)'

    def __str__(self):
        return f"{self.title} - {self.name}"

class SchoolApproval(TimeStampModel):
    """School approval and recognition information"""
    title = models.CharField(max_length=200, default='অনুমোদন', verbose_name='শিরোনাম')
    content = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    image = models.ImageField(
        upload_to='approval_documents/',
        blank=True,
        null=True,
        verbose_name='অনুমোদন দলিল (ছবি)',
        help_text='A4 ratio image of approval document'
    )
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'অনুমোদন'
        verbose_name_plural = 'অনুমোদন'

    def __str__(self):
        return self.title

class SchoolRecognition(TimeStampModel):
    """School recognition and awards"""
    title = models.CharField(max_length=200, default='স্বীকৃতি', verbose_name='শিরোনাম')
    content = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    image = models.ImageField(
        upload_to='recognition_documents/',
        blank=True,
        null=True,
        verbose_name='স্বীকৃতি দলিল (ছবি)',
        help_text='A4 ratio image of recognition document'
    )
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'স্বীকৃতি'
        verbose_name_plural = 'স্বীকৃতি'

    def __str__(self):
        return self.title

class SchoolAims(TimeStampModel):
    """School aims and objectives"""
    title = models.CharField(max_length=200, default='লক্ষ্য ও উদ্দেশ্য', verbose_name='শিরোনাম')
    content = models.TextField(verbose_name='বিস্তারিত বিবরণ')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'লক্ষ্য ও উদ্দেশ্য'
        verbose_name_plural = 'লক্ষ্য ও উদ্দেশ্য'

    def __str__(self):
        return self.title

class AimPoint(TimeStampModel):
    """Individual aim points"""
    aim = models.ForeignKey(SchoolAims, on_delete=models.CASCADE, related_name='points', verbose_name='লক্ষ্য')
    point = models.CharField(max_length=500, verbose_name='লক্ষ্য পয়েন্ট')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    order = models.IntegerField(default=0, verbose_name='ক্রম')

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'লক্ষ্য পয়েন্ট'
        verbose_name_plural = 'লক্ষ্য পয়েন্টসমূহ'

    def __str__(self):
        return self.point

class EventAndNews(models.Model):
    """Events and News model"""
    TYPE_CHOICES = [
        ('EVENT', 'Event'),
        ('NEWS', 'News'),
    ]

    title = models.CharField(max_length=200, verbose_name='শিরোনাম')
    primary_image = models.ImageField(upload_to='event_news_primary/', blank=True, null=True, verbose_name='প্রধান ছবি')
    description = models.TextField(verbose_name='বিবরণ')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True, verbose_name='সক্রিয়')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='ধরন')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ইভেন্ট ও সংবাদ'
        verbose_name_plural = 'ইভেন্ট ও সংবাদসমূহ'

    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"

    @property
    def type_display_bengali(self):
        """Return Bengali display name for type"""
        if self.type == 'EVENT':
            return 'ইভেন্ট'
        elif self.type == 'NEWS':
            return 'সংবাদ'
        return self.get_type_display()


class EventAndNewsImage(models.Model):
    """Gallery images for EventAndNews"""
    event_news = models.ForeignKey(EventAndNews, on_delete=models.CASCADE, related_name='gallery_images', verbose_name='ইভেন্ট ও সংবাদ')
    image = models.ImageField(upload_to='event_news_gallery/', verbose_name='ছবি')
    title = models.CharField(max_length=200, blank=True, verbose_name='ছবির শিরোনাম')
    description = models.TextField(blank=True, verbose_name='ছবির বিবরণ')
    order = models.IntegerField(default=0, verbose_name='ক্রম')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'ইভেন্ট ও সংবাদের ছবি'
        verbose_name_plural = 'ইভেন্ট ও সংবাদের ছবিসমূহ'

    def __str__(self):
        return f"{self.event_news.title} - {self.title or 'Image'}"

# class AboutLink(TimeStampModel):
#     """Important links for about page"""
#     title = models.CharField(max_length=200, verbose_name='লিঙ্কের শিরোনাম')
#     url = models.URLField(verbose_name='লিঙ্ক')
#     is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
#     order = models.IntegerField(default=0, verbose_name='ক্রম')

#     class Meta:
#         ordering = ['order', '-created_at']
#         verbose_name = 'গুরুত্বপূর্ণ লিঙ্ক'
#         verbose_name_plural = 'গুরুত্বপূর্ণ লিঙ্কসমূহ'

#     def __str__(self):
#         return self.title