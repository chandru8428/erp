from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import User  #

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None, **extra_fields):
        user: "User" = self.model(email=email, username=username, **extra_fields)
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()  

    def __str__(self):
        return self.email

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=20)
    admission_year = models.IntegerField()
    dob = models.DateField()
    department = models.CharField(max_length=100)
    degree = models.CharField(max_length=50)
    branch = models.CharField(max_length=100)
    year = models.IntegerField()
    semester = models.CharField(max_length=10)
    section = models.CharField(max_length=10, default='A')
    admission_status = models.CharField(max_length=20, choices=[
        ('Admitted', 'Admitted'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    ], default='Admitted')

    def __str__(self):
        return f"{self.user.username} - {self.reg_no}"



class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=50)  # Lecturer, Asst Prof, etc.

    def __str__(self):
        return self.user.username



class HOD(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username



class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    relation = models.CharField(max_length=50) 
    phone = models.IntegerField() # Father, Mother, etc.

    def __str__(self):
        return f"{self.user.username} ({self.relation})"



class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20)
    phone = models.IntegerField() 
    def __str__(self):
        return self.user.username



class Accountant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    employee_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username


class TransportStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20)
    assigned_route = models.CharField(max_length=100)
    phone = models.IntegerField() 

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=9)  # e.g., 2024-25

    def __str__(self):
        return f"{self.name} ({self.academic_year})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Timetable(models.Model):
    DAYS = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
    ]
    class_section = models.CharField(max_length=100)
    day = models.CharField(max_length=3, choices=DAYS)
    period = models.IntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.class_section} - {self.day} - P{self.period}"

class Attendance(models.Model):
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"


class Fee(models.Model):
    STATUS_CHOICES = [('Paid', 'Paid'), ('Pending', 'Pending')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.user.username} - {self.status}"


class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.course.name} Exam on {self.date}"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField()
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}"



class Book(models.Model):
    isbn = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.book.title} issued to {self.borrower.username}"


class Vehicle(models.Model):
    route = models.CharField(max_length=100)
    driver = models.CharField(max_length=100)

    def __str__(self):
        return self.route

class TransportAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.user.username} - {self.vehicle.route}"


class HostelRoom(models.Model):
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return self.room_number

class HostelAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(HostelRoom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.user.username} - Room {self.room.room_number}"


class Announcement(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    target_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
