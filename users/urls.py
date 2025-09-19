from django.urls import path
from .views import RegisterUser, upload_document, upload_document_page, view_document, RegisterPage, LoginUser, LoginPage, LogoutPage, LogoutUser, okk, profile_view


urlpatterns = [    
    path('', LoginPage.as_view(), name='login_page'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterPage, name='register_page'),
    path('registration/', RegisterUser.as_view(), name='register'),
    path('upload-page/', upload_document_page, name='upload_page'),
    path('upload-document/', upload_document, name='upload_document'),
    path('view-document/', view_document, name='view_document'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('logout-page/', LogoutPage.as_view(), name='logout_page'),
    path('profile_view/', profile_view, name='profile_page'),
    path('okk/', okk, name='okk'),
]
