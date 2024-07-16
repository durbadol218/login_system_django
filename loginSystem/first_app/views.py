from django.shortcuts import render,redirect
from .forms import RegisterForm,UpdateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash


from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse  
# Create your views here.

def home(request):
    return render(request, './home.html')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Congratulations! Account created successfully!')
                form.save(commit=True)
                print(form.cleaned_data)
                return redirect('profile')
            else:
                messages.error(request, 'Please provide valid information!')
        else:
            form = RegisterForm()
        return render(request, './signup.html',{'form':form})
    else:
        return redirect('profile')
        
def userLogin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request,data = request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                user = authenticate(username = name, password=userpass) # check kortesi user ase kina!
                if user is not None:
                    login(request,user)
                    messages.success(request, 'User login successful!')
                    return redirect('profile')
                else:
                    messages.error(request, 'User not found!')
            else:
                messages.error(request, 'Invalid username or password!')
        else:
            form = AuthenticationForm()
        return render(request, './login.html',{'form':form})
    else:
        return redirect('profile')
    
def userLogout(request):
    logout(request)
    return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        return render(request, './profile.html',{'user':request.user})
    else:
        messages.error(request, 'You have need to login first!')
        return redirect('login')

@login_required(login_url='login') #only users can change his/her password!
def changePassword(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = PasswordChangeForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Your password has been changed successfully(with old password)!')
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request,'./passchange.html',{'form':form})
    else:
        return redirect('login')


@login_required(login_url='login') #only users can change his/her password!
def setPassword(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form = SetPasswordForm(user=request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Your password has been changed successfully!')
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request,'./passchange.html',{'form':form})
    else:
        return redirect('login')
    
@login_required(login_url='login')
def updateUser(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateUserForm(request.POST,instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile updated successfully!')
                print(form.cleaned_data)
                return redirect('profile')
            else:
                messages.error(request, 'Sorry,Your profile was not updated!')
        else:
            form = UpdateUserForm(instance=request.user)
        return render(request,'./updateUser.html',{'form':form})
    else:
        redirect('signup')
        
        
def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    sb = "Password reset requested"
                    email_template_name = './password_reset_email.txt'
                    c={
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name':'Website',
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'user':user,
                        'token':default_token_generator.make_token(user),
                        'protocol':'http',
                    }
                    email = render_to_string(email_template_name,c)
                    try:
                        send_mail(subject,email,'goswamidurbadol@gmail.com',[user.email],fail_silently=False)
                    except:
                        return HttpResponse('Invalid header found!')
                    return redirect("/reset_password/done/")
    password_reset_form=PasswordResetForm()
    return render(request,template_name='password_reset.html',context={"password_reset_form":password_reset_form})