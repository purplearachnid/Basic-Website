from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import fitz  # PyMuPDF for PDF handling
from django.core.files.storage import FileSystemStorage
import mysql.connector
from .forms import RegisterForm, LoginForm, PDFUploadForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UploadedPDF
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from django.template.loader import render_to_string


def home(request):
    return render(request, 'converter/home.html')


def pdf_to_text(request):
    return HttpResponse("<h1>Upload your PDF to convert</h1>")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pdf_upload')  
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "converter/login.html")

def register_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, "converter/register.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

def forgot_password_view(request):
    return render(request, 'converter/forgot_password.html')


class CustomPasswordResetView(PasswordResetView):
    template_name = "converter/forgot_password.html"

def custom_password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://127.0.0.1:8000/password-reset-confirm/{uid}/{token}/"

            return render(request, "converter/show_reset_link.html", {"reset_link": reset_link})

        return render(request, "converter/forgot_password.html", {"error": "No account found with this email."})

    return render(request, "converter/forgot_password.html")

def pdf_to_text(request):
    text = None
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        filepath = fs.path(filename)

        with fitz.open(filepath) as doc:
            text = "\n".join([page.get_text() for page in doc])

        fs.delete(filename)  # Clean up file after processing

    return render(request, 'converter/pdf_to_text.html', {'text': text})


@login_required
def pdf_upload(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.user = request.user
            pdf.save()
            return redirect('pdf_history')  # Redirect to history page
    else:
        form = PDFUploadForm()
    
    return render(request, 'converter/pdf_upload.html', {'form': form})

def convert_pdf(request):
    if request.method == "POST":
        pdf_file = request.FILES['pdf_file']
        # PDF processing logic goes here
        return render(request, 'converter/result.html', {'text': "Converted text here"})  # Replace with actual conversion logic

    return redirect('pdf_upload')

@login_required
def pdf_history(request):
    uploaded_pdfs = UploadedPDF.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'converter/pdf_history.html', {'uploaded_pdfs': uploaded_pdfs})

def admin_required(user):
    return user.is_staff  

@user_passes_test(admin_required)
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")