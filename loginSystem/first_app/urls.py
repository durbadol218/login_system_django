from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('signup/', views.signup,name="signup"),
    path('login/', views.userLogin,name="login"),
    path('logout/', views.userLogout,name="logout"),
    path('profile/', views.profile,name="profile"),
    path('passwordChange/', views.changePassword,name="passwordChange"),
    path('setPasswordChange/', views.setPassword,name="setPasswordChange"),
    path('updateUser', views.updateUser, name='updateUser'),
    
    
    path('reset_password/',views.password_reset_request, name="reset_password"),
    # path('reset_password/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name="reset_password"), # submit email form
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"), # email sent success messages
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name="password_reset_confirm"), # Link to password rest form in email
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"), # password successfully changes message
]