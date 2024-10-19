from django.shortcuts import render,redirect
from django.views.generic import View
from .forms import RegisterForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.


class RegisterView(View):
    def post(self,request):
        form = RegisterForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print(form)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username  = email.split('@')[0]

            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)

            user.phone_number= phone_number

            user.save()

            current_site=get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email = email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Registration successful. Verify your email address')
            return redirect('accounts:login')
        else:
            print(form.errors)
          

        context = {
        'form':form,
        }
        return render(request,'accounts/register.html',context)
    def get(self, request):
            form = RegisterForm()
            context = {
                'form': form,
            }
            return render(request, 'accounts/register.html', context)

class LoginView(View):
    def get(self, request):
        # Render the login form for GET requests
        
        return render(request, 'accounts/login.html')

    def post(self, request):
        # Process login form for POST requests
        email= request.POST['email']
        password= request.POST['password']

        user = auth.authenticate(request, email=email, password=password)

        if user is not None:
                # Log the user in
            auth.login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to the homepage or another page
        else:
            # If the credentials are incorrect, show an error message
            messages.error(request, 'Invalid email or password.')
            
            return redirect('accounts:login')  # Redirect to the homepage or another page
        
        
class LogoutView(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'Logout successful!')
        return redirect('accounts:login')
    
class ActivateAccountView(View):
    def get(request,uidb64,token):
        try:
            uid= urlsafe_base64_decode(uidb64).decode()
            user = Account._default_manager.get(pk=uid)
        except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
            user=None


        if user and default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request, 'Your account is activated')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid or expired Activation link')
            return redirect('accounts:login')