"""
URL configuration for first project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from mainapp.views import current_datetime,show_html,signup_view,login_view,landingpage_view,admindashboard_view,extraction_view,upload_pdf,view_imp_questions,similarity_func,view_questions,check_email,view_forget,email_presence
from mainapp.views import get_choices,view_dropdown,addsub_details,view_addsub,checking_code,view_extraction,generate_pdf,visualize_embeddings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cdt/',current_datetime),
    path('show/',show_html),
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('forgetpassword/',view_forget,name="forgetpassword"),
    path('landingpage/',landingpage_view,name='landingpage'),
    path('admindashboard/',admindashboard_view,name='admindashboard'),
    path('extraction/',extraction_view,name="extraction"),
    path('viewextraction/',view_extraction),
    path('upload/', upload_pdf, name='upload_pdf'),
    path('impquestions/',view_imp_questions,name="view"),
    path('generate_new/',similarity_func,name='generate'),
    path('viewquestions/',view_questions),
    path('check_mail/',check_email,name="check_mail"),
    path('mail/',email_presence,name='email_checking'),
    path('get-choices/',get_choices, name='get_choices'),
    path('view-dropdown/',view_dropdown),
    path('add_details/',addsub_details,name="addsubdetails"),
    path('viewadddetails/',view_addsub),
    path('check_code/',checking_code,name="check_code_name"),
    path('downloading/',generate_pdf,name="downloadit"),
    path('visualize/', visualize_embeddings, name='visualize_embeddings'),
]
