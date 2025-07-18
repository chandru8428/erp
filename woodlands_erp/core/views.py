from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import LoginForm 
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import User, Role, Faculty, Parent, Librarian, Accountant, TransportStaff, HOD
from .forms import UserForm, FacultyForm, ParentForm, LibrarianForm, AccountantForm, TransportStaffForm, HODForm
from .models import Student  
from .forms import StudentForm 



def is_superadmin(user):
    return getattr(user.role, 'name', '').lower() == 'super admin'

def login_view(request):  
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('redirect_dashboard')
        else:
            form.add_error(None, 'Invalid credentials')

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def redirect_dashboard(request):
    user = request.user
    role = getattr(user.role, 'name', '').lower()
    if not user.role:
        return redirect('login')
    
    if role == 'student':
        return redirect('student_dashboard')
    elif role == 'faculty':
        return redirect('faculty_dashboard')
    elif role in ['hod', 'principal']:
        return redirect('hod_dashboard')
    elif role == 'parent':
        return redirect('parent_dashboard')
    elif role == 'librarian':
        return redirect('librarian_dashboard')
    elif role == 'accountant':
        return redirect('accountant_dashboard')
    elif role == 'transport':
        return redirect('transport_dashboard')
    elif role == 'super admin':
        return redirect('/admin/')
    else:
        return logout_view(request)

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'core/students/list.html', {'students': students})

@login_required
def student_add(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.role = Role.objects.get(name='Student')
            user.set_password("student123")
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            return redirect('student_list')
    else:
        user_form = UserForm()
        student_form = StudentForm()
    return render(request, 'core/students/add.html', {
        'user_form': user_form,
        'student_form': student_form
    })

@login_required
def student_edit(request, pk):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")
    
    student = get_object_or_404(Student, pk=pk)
    user = student.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        student_form = StudentForm(request.POST, instance=student)
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            return redirect('student_list')
    else:
        user_form = UserForm(instance=user)
        student_form = StudentForm(instance=student)
    return render(request, 'core/students/edit.html', {
        'user_form': user_form,
        'student_form': student_form
    })

@login_required
def student_delete(request, pk):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")

    student = get_object_or_404(Student, pk=pk)
    user = student.user
    if request.method == 'POST':
        student.delete()
        user.delete()
        return redirect('student_list')
    return render(request, 'core/students/delete.html', {'student': student})


@login_required
def faculty_list(request):
    faculties = Faculty.objects.all()
    return render(request, 'core/faculty/list.html', {'faculties': faculties})

@login_required
def faculty_add(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        faculty_form = FacultyForm(request.POST)
        if user_form.is_valid() and faculty_form.is_valid():
            user = user_form.save(commit=False)
            user.role = Role.objects.get(name='Faculty')
            user.set_password("faculty123")
            user.save()
            faculty = faculty_form.save(commit=False)
            faculty.user = user
            faculty.save()
            return redirect('faculty_list')
    else:
        user_form = UserForm()
        faculty_form = FacultyForm()
    return render(request, 'core/faculty/add.html', {
        'user_form': user_form,
        'faculty_form': faculty_form
    })

@login_required
def faculty_edit(request, pk):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")
    
    faculty = get_object_or_404(Faculty, pk=pk)
    user = faculty.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        faculty_form = FacultyForm(request.POST, instance=faculty)
        if user_form.is_valid() and faculty_form.is_valid():
            user_form.save()
            faculty_form.save()
            return redirect('faculty_list')
    else:
        user_form = UserForm(instance=user)
        faculty_form = FacultyForm(instance=faculty)
    return render(request, 'core/faculty/edit.html', {
        'user_form': user_form,
        'faculty_form': faculty_form
    })

@login_required
def faculty_delete(request, pk):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")
    
    faculty = get_object_or_404(Faculty, pk=pk)
    user = faculty.user
    if request.method == 'POST':
        faculty.delete()
        user.delete()
        return redirect('faculty_list')
    return render(request, 'core/faculty/delete.html', {'faculty': faculty})

@login_required
def student_dashboard(request):
    return render(request, 'dashboards/student_dashboard.html')

@login_required
def faculty_dashboard(request):
    return render(request, 'dashboards/faculty_dashboard.html')

@login_required
def hod_dashboard(request):
    return render(request, 'dashboards/hod_dashboard.html')

@login_required
def parent_dashboard(request):
    return render(request, 'dashboards/parent_dashboard.html')

@login_required
def librarian_dashboard(request):
    return render(request, 'dashboards/librarian_dashboard.html')

@login_required
def accountant_dashboard(request):
    return render(request, 'dashboards/accountant_dashboard.html')

@login_required
def transport_dashboard(request):
    return render(request, 'dashboards/transport_dashboard.html')

@login_required
def parent_list(request):
    parents = Parent.objects.all()
    return render(request, 'core/parents/list.html', {'parents': parents})

@login_required
def hod_list(request):
    hods = HOD.objects.all()
    return render(request, 'core/hods/list.html', {'hods': hods})

@login_required
def hod_add(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        hod_form = HODForm(request.POST)
        if user_form.is_valid() and hod_form.is_valid():
            user = user_form.save(commit=False)
            user.role = Role.objects.get(name='HOD')
            user.set_password("hod123")
            user.save()
            hod = hod_form.save(commit=False)
            hod.user = user
            hod.save()
            return redirect('hod_list')
    else:
        user_form = UserForm()
        hod_form = HODForm()
    return render(request, 'core/hods/add.html', {'user_form': user_form, 'hod_form': hod_form})

@login_required
def hod_edit(request, pk):
    hod = get_object_or_404(HOD, pk=pk)
    user = hod.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        hod_form = HODForm(request.POST, instance=hod)
        if user_form.is_valid() and hod_form.is_valid():
            user_form.save()
            hod_form.save()
            return redirect('hod_list')
    else:
        user_form = UserForm(instance=user)
        hod_form = HODForm(instance=hod)
    return render(request, 'core/hods/edit.html', {'user_form': user_form, 'hod_form': hod_form})

@login_required
def hod_delete(request, pk):
    hod = get_object_or_404(HOD, pk=pk)
    user = hod.user
    if request.method == 'POST':
        hod.delete()
        user.delete()
        return redirect('hod_list')
    return render(request, 'core/hods/delete.html', {'hod': hod})

@login_required
def parent_add(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        parent_form = ParentForm(request.POST)
        if user_form.is_valid() and parent_form.is_valid():
            user = user_form.save(commit=False)
            user.role = Role.objects.get(name='Parent')
            user.set_password("parent123")  
            user.save()
            parent = parent_form.save(commit=False)
            parent.user = user
            parent.save()
            return redirect('parent_list')
    else:
        user_form = UserForm()
        parent_form = ParentForm()
    return render(request, 'core/parents/add.html', {
        'user_form': user_form,
        'parent_form': parent_form
    })


@login_required
def parent_edit(request, pk):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")

    parent = get_object_or_404(Parent, pk=pk)
    user = parent.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        parent_form = ParentForm(request.POST, instance=parent)
        if user_form.is_valid() and parent_form.is_valid():
            user_form.save()
            parent_form.save()
            return redirect('parent_list')
    else:
        user_form = UserForm(instance=user)
        parent_form = ParentForm(instance=parent)
    return render(request, 'core/parents/edit.html', {
        'user_form': user_form,
        'parent_form': parent_form
    })


@login_required
def parent_delete(request, pk):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")

    parent = get_object_or_404(Parent, pk=pk)
    user = parent.user
    if request.method == 'POST':
        parent.delete()
        user.delete()
        return redirect('parent_list')
    return render(request, 'core/parents/delete.html', {'parent': parent})

from .models import Librarian, Role, User
from .forms import UserForm, LibrarianForm

def is_superadmin(user):
    return user.role.name.lower() == 'super admin'

@login_required
def librarian_list(request):
    librarians = Librarian.objects.all()
    return render(request, 'core/librarians/list.html', {'librarians': librarians})

@login_required
def librarian_add(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        librarian_form = LibrarianForm(request.POST)
        if user_form.is_valid() and librarian_form.is_valid():
            user = user_form.save(commit=False)
            user.role = Role.objects.get(name='Librarian')
            user.set_password("librarian123")
            user.save()
            librarian = librarian_form.save(commit=False)
            librarian.user = user
            librarian.save()
            return redirect('librarian_list')
    else:
        user_form = UserForm()
        librarian_form = LibrarianForm()
    return render(request, 'core/librarians/add.html', {
        'user_form': user_form,
        'librarian_form': librarian_form
    })

@login_required
def librarian_edit(request, pk):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")
    
    librarian = get_object_or_404(Librarian, pk=pk)
    user = librarian.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        librarian_form = LibrarianForm(request.POST, instance=librarian)
        if user_form.is_valid() and librarian_form.is_valid():
            user_form.save()
            librarian_form.save()
            return redirect('librarian_list')
    else:
        user_form = UserForm(instance=user)
        librarian_form = LibrarianForm(instance=librarian)
    return render(request, 'core/librarians/edit.html', {
        'user_form': user_form,
        'librarian_form': librarian_form
    })

@login_required
def librarian_delete(request, pk):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")
    
    librarian = get_object_or_404(Librarian, pk=pk)
    user = librarian.user
    if request.method == 'POST':
        librarian.delete()
        user.delete()
        return redirect('librarian_list')
    return render(request, 'core/librarians/delete.html', {'librarian': librarian})

@login_required
def accountant_list(request):
    accountants = Accountant.objects.all()
    return render(request, 'core/accountants/list.html', {'accountants': accountants})

@login_required
def accountant_add(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        accountant_form = AccountantForm(request.POST)
        if user_form.is_valid() and accountant_form.is_valid():
            user = user_form.save(commit=False)
            user.role = Role.objects.get(name='Accountant')
            user.set_password("accountant123")
            user.save()
            accountant = accountant_form.save(commit=False)
            accountant.user = user
            accountant.save()
            return redirect('accountant_list')
    else:
        user_form = UserForm()
        accountant_form = AccountantForm()
    return render(request, 'core/accountants/add.html', {'user_form': user_form, 'accountant_form': accountant_form})

@login_required
def accountant_edit(request, pk):
    accountant = get_object_or_404(Accountant, pk=pk)
    user = accountant.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        accountant_form = AccountantForm(request.POST, instance=accountant)
        if user_form.is_valid() and accountant_form.is_valid():
            user_form.save()
            accountant_form.save()
            return redirect('accountant_list')
    else:
        user_form = UserForm(instance=user)
        accountant_form = AccountantForm(instance=accountant)
    return render(request, 'core/accountants/edit.html', {'user_form': user_form, 'accountant_form': accountant_form})

@login_required
def accountant_delete(request, pk):
    accountant = get_object_or_404(Accountant, pk=pk)
    user = accountant.user
    if request.method == 'POST':
        accountant.delete()
        user.delete()
        return redirect('accountant_list')
    return render(request, 'core/accountants/delete.html', {'accountant': accountant})


@login_required
def transport_list(request):
    transports = TransportStaff.objects.all()
    return render(request, 'core/transports/list.html', {'transports': transports})

@login_required
def transport_add(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        transport_form = TransportStaffForm(request.POST)
        if user_form.is_valid() and transport_form.is_valid():
            user = user_form.save(commit=False)
            user.role = Role.objects.get(name='Transport')
            user.set_password("transport123")
            user.save()
            transport = transport_form.save(commit=False)
            transport.user = user
            transport.save()
            return redirect('transport_list')
    else:
        user_form = UserForm()
        transport_form = TransportStaffForm()
    return render(request, 'core/transports/add.html', {'user_form': user_form, 'transport_form': transport_form})

@login_required
def transport_edit(request, pk):
    transport = get_object_or_404(TransportStaff, pk=pk)
    user = transport.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        transport_form = TransportStaffForm(request.POST, instance=transport)
        if user_form.is_valid() and transport_form.is_valid():
            user_form.save()
            transport_form.save()
            return redirect('transport_list')
    else:
        user_form = UserForm(instance=user)
        transport_form = TransportStaffForm(instance=transport)
    return render(request, 'core/transports/edit.html', {'user_form': user_form, 'transport_form': transport_form})

@login_required
def transport_delete(request, pk):
    transport = get_object_or_404(TransportStaff, pk=pk)
    user = transport.user
    if request.method == 'POST':
        transport.delete()
        user.delete()
        return redirect('transport_list')
    return render(request, 'core/transports/delete.html', {'transport': transport})

@login_required
def librarian_list(request):
    librarians = Librarian.objects.all()
    return render(request, 'core/librarians/list.html', {'librarians': librarians})

@login_required
def librarian_add(request):
    if not is_superadmin(request.user):
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        librarian_form = LibrarianForm(request.POST)
        if user_form.is_valid() and librarian_form.is_valid():
            user = user_form.save(commit=False)
            user.role = Role.objects.get(name='Librarian')
            user.set_password("librarian123")
            user.save()
            librarian = librarian_form.save(commit=False)
            librarian.user = user
            librarian.save()
            return redirect('librarian_list')
    else:
        user_form = UserForm()
        librarian_form = LibrarianForm()
    return render(request, 'core/librarians/add.html', {'user_form': user_form, 'librarian_form': librarian_form})

@login_required
def librarian_edit(request, pk):
    librarian = get_object_or_404(Librarian, pk=pk)
    user = librarian.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        librarian_form = LibrarianForm(request.POST, instance=librarian)
        if user_form.is_valid() and librarian_form.is_valid():
            user_form.save()
            librarian_form.save()
            return redirect('librarian_list')
    else:
        user_form = UserForm(instance=user)
        librarian_form = LibrarianForm(instance=librarian)
    return render(request, 'core/librarians/edit.html', {'user_form': user_form, 'librarian_form': librarian_form})

@login_required
def librarian_delete(request, pk):
    librarian = get_object_or_404(Librarian, pk=pk)
    user = librarian.user
    if request.method == 'POST':
        librarian.delete()
        user.delete()
        return redirect('librarian_list')
    return render(request, 'core/librarians/delete.html', {'librarian': librarian})

