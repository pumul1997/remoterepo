from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from admin import views
from e_biding import settings

urlpatterns = [
    path('', TemplateView.as_view(template_name="admin/index.html"),name="index"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('admin_logout/', views.admin_logout, name="admin_logout"),
    path('welcome/', views.welcome, name="welcome"),
    path('pending_req/', views.pending_req, name="pending_req"),
    path('approved_req/', views.approved_req, name="approved_req"),
    path('declined_req/', views.declined_req, name="declined_req"),
    path('approve/<int:pk>/', views.approve, name="approve"),
    path('decline/<int:pk><str:name>/', views.decline, name="decline"),
    path('decline_confirm/<int:pk>/', views.decline_confirm, name="decline_confirm"),
    path('change_pass/', views.changepass, name="change_pass"),
    path('complain/', views.complain, name="complain"),
    path('del_complain/<int:pk>/', views.del_complain, name="del_complain"),
    path('contact/', views.contact_page, name="contact"),
    path('about/', views.about, name="about"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
