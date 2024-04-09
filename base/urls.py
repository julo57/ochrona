from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
  
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('documents/upload/', views.document_upload, name='document_upload'),
    path('documents/', views.document_list, name='documents'),
      path('documents/edit/<int:document_id>/', views.document_edit, name='document_edit'),
       path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('edit_user_role/<int:user_id>/', views.edit_user_role, name='edit_user_role'),
    path('folders/', views.folder_list, name='folders'),  # Dodanie ukośnika na końcu
    path('folder/<str:department>/', views.folder_detail, name='folder_detail'),
  
    path('folders/IT/', views.folder_content_view, {'folder_name': 'IT'}, name='folder_it'),
    path('folders/Sales/', views.folder_content_view, {'folder_name': 'Sales'}, name='folder_sales'),
    path('folders/HR/', views.folder_content_view, {'folder_name': 'HR'}, name='folder_hr'),
    path('documents/replace/<int:document_id>/', views.document_replace, name='document_replace'),
]