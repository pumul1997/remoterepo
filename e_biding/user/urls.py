from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from user import views
from e_biding import settings

urlpatterns = [
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('profile/', views.profile, name="profile"),
    path('registration_page/', views.registration_page, name="registration_page"),
    path('register/', views.register, name="register"),
    path('upload/', views.upload, name="upload"),
    path('user_change_pass/', views.user_changepass, name="user_change_pass"),
    path('seller/', views.seller, name="seller"),
    path('buyer/', views.buyer, name="buyer"),
    path('add_product/', views.add_product, name="add_product"),
    path('update_pro/', views.update_pro, name="update_pro"),
    path('delete_pro/', views.delete_pro, name="delete_pro"),
    path('delete<int:pk>/', views.delete, name="delete"),
    path('update/', views.update, name="update"),
    path('my_product/', views.my_product, name="my_product"),
    path('bid_product/', views.bid_product, name="bid_product"),
    path('not_bid_product/', views.not_bid_product, name="not_bid_product"),
    path('sold_product/', views.sold_product, name="sold_product"),
    path('bidding<int:pk>/', views.bidding, name="bidding"),
    path('bidding_process/', views.bidding_process, name="bidding_process"),
    path('bidding_details<int:pk>/', views.bidding_details, name="bidding_details"),
    path('my_cart/', views.my_cart, name="my_cart"),
    path('stop_bid<int:pk>/', views.stop_bid, name="stop_bid"),
    path('checkout_page<int:pk>/', views.checkout_page, name="checkout_page"),
    path('checkout/', views.checkout, name="checkout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
