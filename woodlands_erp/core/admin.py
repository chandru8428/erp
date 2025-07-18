from django.contrib import admin
from .models import *

# Common config base
class DefaultAdmin(admin.ModelAdmin):
    list_per_page = 25

# Role & User
@admin.register(Role)
class RoleAdmin(DefaultAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(User)
class UserAdmin(DefaultAdmin):
    list_display = ['id', 'username', 'email', 'role']
    search_fields = ['username', 'email']
    list_filter = ['role']

    def save_model(self, request, obj, form, change):
        if obj.role and not Role.objects.filter(id=obj.role.id).exists():
            obj.role = None  
        super().save_model(request, obj, form, change)

# Faculty & Student
@admin.register(Faculty)
class FacultyAdmin(DefaultAdmin):
    list_display = ['id', 'user', 'department']
    search_fields = ['user__username', 'department']

@admin.register(Student)
class StudentAdmin(DefaultAdmin):
    list_display = ['id', 'user', 'section', 'admission_status']
    search_fields = ['user__username', 'section']
    list_filter = ['section', 'admission_status']

# Course & Subject
@admin.register(Course)
class CourseAdmin(DefaultAdmin):
    list_display = ['id', 'name', 'academic_year']
    search_fields = ['name', 'academic_year']

@admin.register(Subject)
class SubjectAdmin(DefaultAdmin):
    list_display = ['id', 'name', 'course', 'faculty']
    search_fields = ['name']
    list_filter = ['course']

# Timetable
@admin.register(Timetable)
class TimetableAdmin(DefaultAdmin):
    list_display = ['id', 'class_section', 'day', 'period', 'subject']
    list_filter = ['class_section', 'day']

# Attendance
@admin.register(Attendance)
class AttendanceAdmin(DefaultAdmin):
    list_display = ['id', 'student', 'subject', 'date', 'status', 'period']
    list_filter = ['date', 'subject', 'status']
    search_fields = ['student__user__username']

# Fees
@admin.register(Fee)
class FeeAdmin(DefaultAdmin):
    list_display = ['id', 'student', 'amount', 'due_date', 'status']
    list_filter = ['status']
    search_fields = ['student__user__username']

# Exams & Results
@admin.register(Exam)
class ExamAdmin(DefaultAdmin):
    list_display = ['id', 'course', 'date']
    list_filter = ['course']

@admin.register(Result)
class ResultAdmin(DefaultAdmin):
    list_display = ['id', 'student', 'subject', 'marks', 'grade']
    list_filter = ['grade']
    search_fields = ['student__user__username', 'subject__name']

# Library
@admin.register(Book)
class BookAdmin(DefaultAdmin):
    list_display = ['id', 'isbn', 'title', 'author']
    search_fields = ['title', 'isbn']

@admin.register(Issue)
class IssueAdmin(DefaultAdmin):
    list_display = ['id', 'book', 'borrower', 'issue_date', 'return_date', 'fine']
    list_filter = ['issue_date', 'return_date']

# Hostel & Transport
@admin.register(Vehicle)
class VehicleAdmin(DefaultAdmin):
    list_display = ['id', 'route', 'driver']
    search_fields = ['route']

@admin.register(TransportAssignment)
class TransportAssignmentAdmin(DefaultAdmin):
    list_display = ['id', 'student', 'vehicle']
    search_fields = ['student__user__username']

@admin.register(HostelRoom)
class HostelRoomAdmin(DefaultAdmin):
    list_display = ['id', 'room_number', 'capacity']

@admin.register(HostelAssignment)
class HostelAssignmentAdmin(DefaultAdmin):
    list_display = ['id', 'student', 'room']

# Announcements
@admin.register(Announcement)
class AnnouncementAdmin(DefaultAdmin):
    list_display = ['id', 'title', 'posted_by', 'target_role']
    search_fields = ['title']
