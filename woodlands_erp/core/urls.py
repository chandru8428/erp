from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('redirect/', views.redirect_dashboard, name='redirect_dashboard'),

    
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('dashboard/hod/', views.hod_dashboard, name='hod_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
    path('dashboard/librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('dashboard/accountant/', views.accountant_dashboard, name='accountant_dashboard'),
    path('dashboard/transport/', views.transport_dashboard, name='transport_dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/add/', views.faculty_add, name='faculty_add'),
    path('faculty/edit/<int:pk>/', views.faculty_edit, name='faculty_edit'),
    path('faculty/delete/<int:pk>/', views.faculty_delete, name='faculty_delete'),
    path('hods/', views.hod_list, name='hod_list'),
    path('hods/add/', views.hod_add, name='hod_add'),
    path('hods/edit/<int:pk>/', views.hod_edit, name='hod_edit'),
    path('hods/delete/<int:pk>/', views.hod_delete, name='hod_delete'),
    path('parents/', views.parent_list, name='parent_list'),
    path('parents/add/', views.parent_add, name='parent_add'),
    path('parents/edit/<int:pk>/', views.parent_edit, name='parent_edit'),
    path('parents/delete/<int:pk>/', views.parent_delete, name='parent_delete'),
    path('librarians/', views.librarian_list, name='librarian_list'),
    path('librarians/add/', views.librarian_add, name='librarian_add'),
    path('librarians/edit/<int:pk>/', views.librarian_edit, name='librarian_edit'),
    path('librarians/delete/<int:pk>/', views.librarian_delete, name='librarian_delete'),

]
