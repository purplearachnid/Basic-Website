from django.contrib.auth import views as auth_views  
from django.urls import path
from . import views 
from .views import convert_pdf,pdf_upload, pdf_history, admin_dashboard, custom_password_reset

urlpatterns = [
    path('', views.home, name='home'),
    path('convert/', views.pdf_to_text, name='pdf_to_text'),  
    path('login/', views.login_view, name='login'),
    path('upload/', views.pdf_upload, name="pdf_upload"),
    path("history/", views.pdf_history, name="pdf_history"),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('convert/', convert_pdf, name='convert_pdf'),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("forgot-password/", custom_password_reset, name="forgot_password"),
]

urlpatterns += [
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
