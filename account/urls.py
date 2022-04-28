from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_attempts, name='login'),
    path('signup', register_attempts, name='signup'),
    path('token_send', token_send, name='token_send'),
    path('success', success, name='success'),
    path('verify/<auth_token>', verify, name='verify'),
    path('error', error_page, name='error'),
    path('logout', logout_view, name='logout'),
    path('changepassword/<token>', changepassword, name='changepassword'),
    path('forgetpassword', forgetpassword, name='forgetpassword'),
    path('contact', contactus, name='contact'),
    path('aboutus', aboutus, name='aboutus'),
]
# <token >
