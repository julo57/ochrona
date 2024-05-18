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
    path('folders/', views.folder_list, name='folders'),
    path('folder/<str:department>/', views.folder_detail, name='folder_detail'),
    path('documents/replace/<int:document_id>/', views.document_replace, name='document_replace'),
    path('send-document/', views.send_document, name='send_document'),
    path('send-key/', views.send_key, name='send_key'),
    path('received-documents/', views.list_received_documents, name='received-documents'),
    path('received-keys/', views.list_received_keys, name='received-keys'),
    path('upload_public_key/', views.upload_public_key, name='upload_public_key'),
]
