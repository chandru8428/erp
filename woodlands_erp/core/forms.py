from django import forms
from .models import User, Faculty,Accountant, Student,HOD , Librarian, Parent, Accountant, Student,HOD,TransportStaff
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    email = forms.EmailField() 
    password = forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['department', 'designation', 'emp_id']

class HODForm(forms.ModelForm):
    class Meta:
        model = HOD
        fields = ['department'] #

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['phone']

class LibrarianForm(forms.ModelForm):
    class Meta:
        model = Librarian
        fields = ['phone', 'employee_id']

class AccountantForm(forms.ModelForm):
    class Meta:
        model = Accountant
        fields = ['phone', 'employee_id']

class TransportStaffForm(forms.ModelForm):
    class Meta:
        model = TransportStaff
        fields = ['phone', 'employee_id']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'reg_no', 'degree', 'branch', 'year', 'semester', 'section', 'admission_year', 'dob']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }
