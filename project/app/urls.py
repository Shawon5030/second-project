from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.conf.urls.static import static
from .form import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='index'),
    path('home/', home, name='home'),
    path('form/', Cform, name='form'),
    path('formSubmit', formsee, name='formSubmit'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm) , name='login'),
    path('registration/', CustomerRegistrationView.as_view(), name='customerregistration'),
    
    path('profile/' , user_form_view , name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    
    
    
    path('show/customer/data', show_customer_data, name='show_customer_data'),
    path('withdraw/', withdraw_request, name='withdraw'),
    path('withdrawal-history/', withdrawal_history, name='withdrawal_history'),
    path('withdrawal/<int:withdrawal_id>/invoice/', generate_invoice, name='generate_invoice'),
    
    
   
   
    

    
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)