# Temporarily disabled signals since we're handling foreign key updates directly in admin
# from django.db.models.signals import pre_delete
# from django.dispatch import receiver
# from django.db import connection
# from .models import Class, Department


# @receiver(pre_delete, sender=Class)
# def handle_class_pre_delete(sender, instance, **kwargs):
#     """
#     Handle Class deletion by setting all related foreign keys to NULL
#     """
#     try:
#         with connection.cursor() as cursor:
#             # Temporarily disable foreign key constraints
#             cursor.execute("PRAGMA foreign_keys=OFF")
            
#             # Update all related objects to set class foreign keys to NULL
#             instance.student_set.update(class_name=None)
#             instance.routine_set.update(class_name=None)
#             instance.book_set.update(class_name=None)
#             instance.syllabus_set.update(class_name=None)
#             instance.result_set.update(class_name=None)
#             instance.admission_set.update(class_name=None)
            
#             # Re-enable foreign key constraints
#             cursor.execute("PRAGMA foreign_keys=ON")
#     except Exception as e:
#         print(f"Error in class pre_delete signal: {e}")


# @receiver(pre_delete, sender=Department)
# def handle_department_pre_delete(sender, instance, **kwargs):
#     """
#     Handle Department deletion by setting all related foreign keys to NULL
#     """
#     try:
#         with connection.cursor() as cursor:
#             # Temporarily disable foreign key constraints
#             cursor.execute("PRAGMA foreign_keys=OFF")
            
#             # Update all related objects to set department foreign keys to NULL
#             instance.student_set.update(department=None)
#             instance.routine_set.update(department=None)
#             instance.book_set.update(department=None)
#             instance.syllabus_set.update(department=None)
#             instance.result_set.update(department=None)
#             instance.admission_set.update(department=None)
            
#             # Re-enable foreign key constraints
#             cursor.execute("PRAGMA foreign_keys=ON")
#     except Exception as e:
#         print(f"Error in department pre_delete signal: {e}")
