from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponse
from .forms import ProfileForm, LoginForm,DocumentForm,UserRoleForm,SendDocumentForm
from .models import Profile, HRDocument, ITDocument, SalesDocument, FinanceDocument, LogisticsDocument
from django.forms.models import modelform_factory
from django.contrib.auth.hashers import check_password
from docx import Document as DocxDocument
import subprocess
import os
from django.conf import settings
from django.contrib import messages
from django.db.models import Q  # Pamiętaj o dodaniu tego importu
from .forms import PublicKeyForm
from .models import SendDocument


def home(request):
    # Twoja logika pozostaje bez zmian do momentu pomyślnego logowania
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = Profile.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    
                    request.session['role'] = user.role
                    return redirect('home')
                else:
                    return HttpResponse("Nieprawidłowa nazwa użytkownika lub hasło.", status=401)
            except Profile.DoesNotExist:
                return HttpResponse("Nie znaleziono użytkownika.", status=404)
    else:
        form = LoginForm()
    return render(request, 'base/home.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm()
    return render(request, 'base/register.html', {'form': form})

def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('home')



def document_upload(request):
    user_profile = get_object_or_404(Profile, id=request.session.get('user_id'))
    document_mapping = {
        'HR': HRDocument,
        'Sales': SalesDocument,
        'IT': ITDocument,
        'FINANCE': FinanceDocument,
        'LOGISTICS': LogisticsDocument
    }

    DocumentModel = document_mapping.get(user_profile.department)
    if not DocumentModel:
        messages.error(request, "Nieznany departament")
        return HttpResponse("Nieznany departament", status=400)
    
    DocumentForm = modelform_factory(DocumentModel, fields=['title', 'file', 'is_public'])

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.author = user_profile
            document.save()
            messages.success(request, "Dokument został pomyślnie przesłany.")
            return redirect('documents')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = DocumentForm()

    return render(request, 'base/document_upload.html', {'form': form})


def get_document_model(user_profile):
    print("Wywołanie get_document_model z profile:", user_profile)
    
    if user_profile.role in ['superadmin']:
        # Jeśli jest adminem, zwróć domyślny model
        return SalesDocument
    elif user_profile.department == 'HR':
        print("Zwracam model HRDocument")
        return HRDocument
    elif user_profile.department == 'Sales':
        print("Zwracam model SALesDocument")
        return SalesDocument
    elif user_profile.department == 'IT':
        print("Zwracam model ITDocument")
        return ITDocument
    elif user_profile.department == 'FINANCE':
        print("Zwracam model FinanceDocument")
        return FinanceDocument
    elif user_profile.department == 'LOGISTICS':
        print("Zwracam model LogisticsDocument")
        return LogisticsDocument
    else:
        # Zabezpieczenie: zwróć domyślny model, jeśli żaden warunek nie został spełniony
        print("Zwracam model ITDocument")
        return SalesDocument


def get_folder_name(user_profile, chosen_folder=None):
    # Funkcja określająca nazwę folderu na podstawie roli/departamentu użytkownika
    # i opcjonalnie wybranego folderu
    if user_profile.role in ['superadmin', 'admin'] and chosen_folder:
        return chosen_folder
    return user_profile.department
def encrypt_file(input_path, output_path, recipient):
    # Funkcja do szyfrowania plików przy użyciu GPG
    gpg_path = 'C:\\Program Files (x86)\\GnuPG\\bin\\gpg.exe'  # Zaktualizuj ścieżkę do GPG
    subprocess.run([gpg_path, '--output', output_path, '--encrypt', '--recipient', recipient, input_path])


def document_list(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    user_id = request.session.get('user_id')
    hr_documents = HRDocument.objects.filter(author_id=user_id)
    sales_documents = SalesDocument.objects.filter(author_id=user_id)
    it_documents = ITDocument.objects.filter(author_id=user_id)

    
    # Możesz połączyć te zapytania w jedną listę, jeśli chcesz je wyświetlić razem
    documents = list(hr_documents) + list(sales_documents) + list(it_documents)
    
    return render(request, 'base/document_list.html', {'documents': documents})


def document_edit(request, document_type, document_id):
    model_mapping = {
        'hr': HRDocument,
        'sales': SalesDocument,
        'it': ITDocument,
        'finance': FinanceDocument,
        'logistics': LogisticsDocument,
    }
    DocumentModel = model_mapping.get(document_type.lower())
    if not DocumentModel:
        return HttpResponse('Niepoprawny typ dokumentu.', status=404)
    
    document = get_object_or_404(DocumentModel, id=document_id, author_id=request.session.get('user_id'))
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save(commit=False)
            document.last_edited_by = request.user.profile
            document.save()
            return redirect('documents')
    else:
        form = DocumentForm(instance=document)
    
    return render(request, 'base/document_edit.html', {'form': form, 'document': document})


def get_document_model(document_type):
    if document_type == 'hr':
        return HRDocument
    elif document_type == 'sales':
        return SalesDocument
    elif document_type == 'it':
        return ITDocument
    else:
        return None

def document_replace(request, document_type, document_id):
    DocumentModel = get_document_model(document_type)
    if DocumentModel is None:
        return HttpResponse("Nieznany typ dokumentu.", status=404)
    
    document = get_object_or_404(DocumentModel, id=document_id, author_id=request.session.get('user_id'))
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            # Zaktualizuj dokument
            updated_document = form.save(commit=False)
            # Tutaj możesz dodać dodatkową logikę, np. zaktualizować ścieżkę pliku po szyfrowaniu
            updated_document.save()
            return redirect('documents')
    else:
        form = DocumentForm(instance=document)
    
    return render(request, 'base/document_replace.html', {'form': form, 'document': document})

def admin_panel(request):
    # Sprawdza, czy użytkownik jest zalogowany
    if not request.session.get('user_id'):
        return redirect('login')  # Przekierowuje do strony logowania, jeśli nie

    user = Profile.objects.get(id=request.session.get('user_id'))
    # Sprawdza, czy zalogowany użytkownik jest superadministratorem
    if user.role != 'superadmin':
        return redirect('home')  # Przekierowuje do strony głównej, jeśli nie

    # Pobiera listę wszystkich użytkowników
    users = Profile.objects.all()
    return render(request, 'base/admin_panel.html', {'users': users})

def edit_user_role(request, user_id):
    # Sprawdza, czy użytkownik jest zalogowany
    if not request.session.get('user_id'):
        return redirect('login')  # Przekierowuje do strony logowania, jeśli nie

    # Pobiera informacje o zalogowanym użytkowniku
    logged_user = Profile.objects.get(id=request.session.get('user_id'))
    if logged_user.role != 'superadmin':
        return redirect('home')  # Przekierowuje do strony głównej, jeśli użytkownik nie jest superadministratorem

    user = get_object_or_404(Profile, id=user_id)
    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = UserRoleForm(instance=user)
    return render(request, 'base/edit_user_role.html', {'form': form, 'user': user})


def folder_list(request):
    if not request.session.get('user_id'):
        return redirect('login')

    user_id = request.session.get('user_id')
    try:
        user_profile = Profile.objects.get(id=user_id)
        user_department = user_profile.department
        folders = ['HR', 'SALES', 'IT','FINANCE','LOGISTICS']
        return render(request, 'base/folders.html', {'folders': folders, 'user_department': user_department})
    except Profile.DoesNotExist:
        return HttpResponse('Nie znaleziono profilu.', status=404)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, ITDocument, HRDocument, SalesDocument

def folder_detail(request, department):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Pobranie profilu zalogowanego użytkownika
    user_profile = get_object_or_404(Profile, id=request.session.get('user_id'))
    
    # Mapowanie nazwy departamentu na odpowiadający mu model dokumentu
    department_to_model = {
        'HR': HRDocument,
        'SALES': SalesDocument,
        'IT': ITDocument,
        'FINANCE': FinanceDocument,
        'LOGISTICS': LogisticsDocument
    }

    DocumentModel = department_to_model.get(department)
    if not DocumentModel:
        return HttpResponse("Nieznany departament", status=400)

    # Sprawdzenie, czy użytkownik ma uprawnienia do przeglądania dokumentów danego departamentu
    if not (user_profile.role in ['superadmin', 'admin'] or user_profile.department == department):
        return HttpResponse("Brak dostępu", status=403)
    
    # Filtracja dokumentów:
    if user_profile.role in ['superadmin', 'admin']:
        # Admini i superadmini widzą wszystkie dokumenty w danym departamencie
        documents = DocumentModel.objects.all()
    else:
        # Pozostali użytkownicy widzą tylko swoje dokumenty i publiczne dokumenty w danym departamencie
        documents = DocumentModel.objects.filter(author=user_profile) | DocumentModel.objects.filter(is_public=True)

    template_name = f'base/departments/{department.lower()}.html'  # Dynamiczne tworzenie nazwy szablonu

    return render(request, template_name, {'department': department, 'documents': documents})


def folders_view(request):
    if not request.session.get('user_id'):
        return redirect('login')
    
    user_id = request.session.get('user_id')
    user = Profile.objects.get(id=user_id)
    
    if user.role in ['superadmin', 'admin']:
        folders = ['IT', 'SALES', 'HR','FINANCE','LOGISTICS']  # Admini mają dostęp do wszystkich folderów
    else:
        folders = [user.department]  # Pracownicy mają dostęp tylko do swojego działu
    
    return render(request, 'folders.html', {'folders': folders})



def get_document_instance_and_model(document_id, user_id):
    # Funkcja próbuje znaleźć instancję dokumentu w różnych modelach
    for Model in [HRDocument, ITDocument, SalesDocument, FinanceDocument, LogisticsDocument]:
        try:
            return Model.objects.get(id=document_id, author_id=user_id), Model
        except Model.DoesNotExist:
            continue
    return None, None

from django.utils import timezone

def document_replace(request, document_id):
    user_id = request.session.get('user_id')
    user_profile = get_object_or_404(Profile, id=user_id)

    # Przypisz model na podstawie departamentu użytkownika
    if user_profile.department == 'HR':
        DocumentModel = HRDocument
    elif user_profile.department == 'Sales':
        DocumentModel = SalesDocument
    elif user_profile.department == 'IT':
        DocumentModel = ITDocument
    elif user_profile.department == 'FINANCE':
        DocumentModel = FinanceDocument
    elif user_profile.department == 'LOGISTICS':
        DocumentModel = LogisticsDocument
    else:
        return HttpResponse("Nieznany departament", status=400)
    
    # Pobierz dokument z odpowiedniego modelu
    document = get_object_or_404(DocumentModel, id=document_id, author=user_profile)

    # Tworzenie formularza dla wybranego modelu
    DocumentForm = modelform_factory(DocumentModel, fields=('title', 'file'))

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            # Usuń stary plik z dysku, jeśli istnieje
            old_file_path = document.file.path
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
                
            updated_document = form.save(commit=False)
            updated_document.last_replaced_by = user_profile
            updated_document.last_replaced_at = timezone.now()  # Zapisz bieżącą datę i czas zastąpienia
            updated_document.save()

            messages.success(request, "Dokument został zastąpiony.")
            return redirect('documents')  # Upewnij się, że 'document_list' to prawidłowa nazwa URL
    else:
        form = DocumentForm(instance=document)

    return render(request, 'base/document_upload.html', {'form': form, 'document': document})



def send_document(request):
    user_profile = get_object_or_404(Profile, id=request.session.get('user_id'))
    department_to_model = {
        'HR': HRDocument,
        'Sales': SalesDocument,
        'IT': ITDocument,
        'FINANCE': FinanceDocument,
        'LOGISTICS': LogisticsDocument,
    }

    DocumentModel = department_to_model.get(user_profile.department)
    if not DocumentModel:
        return HttpResponse("Nieznany departament", status=400)

    if request.method == 'POST':
        form = SendDocumentForm(request.POST, request.FILES, user_profile=user_profile)
        if form.is_valid():
            document = form.save(commit=False)
            document.author = user_profile
            document.public_key = form.cleaned_data['public_key']  # Przypisanie wybranego klucza publicznego
            document.save()  # Zapisujemy dokument przed przypisaniem relacji wiele-do-wielu
            
            # Obsługa wielu odbiorców
            recipients = form.cleaned_data['recipients']
            document.recipients.set(recipients)  # Ustawienie wielu odbiorców
            
            # Możesz tutaj dodać wiadomość o sukcesie lub podobną logikę.
            return redirect('home')
    else:
        form = SendDocumentForm(user_profile=user_profile)

    return render(request, 'base/send_document.html', {'form': form})

def list_received_documents(request):
    user_profile = get_object_or_404(Profile, id=request.session.get('user_id'))  # Pobranie profilu zalogowanego użytkownika

    # Pobieranie dokumentów przypisanych do profilu użytkownika jako pojedynczego odbiorcę lub jako jednego z wielu odbiorców
    documents = SendDocument.objects.filter(
        Q(recipient=user_profile) | Q(recipients=user_profile)
    ).distinct()

    return render(request, 'base/received_documents.html', {'documents': documents})

def upload_public_key(request):
    user_profile = get_object_or_404(Profile, id=request.session.get('user_id'))
    
    if request.method == 'POST':
        form = PublicKeyForm(request.POST, profile=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Przekierowanie do strony głównej po pomyślnym dodaniu lub aktualizacji klucza
    else:
        form = PublicKeyForm(profile=user_profile)  # Przekazanie profilu również przy tworzeniu pustego formularza

    return render(request, 'base/upload_key.html', {'form': form})