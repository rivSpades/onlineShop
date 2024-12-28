from django.shortcuts import render,redirect
from django.views.generic import View
from .forms import RegisterForm
from .models import Account
from cart.models import Cart,CartItem
from django.contrib import messages,auth
from django.contrib.auth import get_user_model,authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import RegisterSerializer, LoginSerializer, ResetPasswordSerializer
import jwt
from .tokens import account_activation_token
from .utils import send_activation_email

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
        
class DashboardView(View):
    @method_decorator(login_required(login_url='accounts:login'))
    def get(self,request):
       
       
        return render(request,'accounts/dashboard.html')        
    
class ForgotPasswordView(View):
    
    def post(self,request):
        email= request.POST['email']
        
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__iexact=email)
            current_site=get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email = email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()            
            messages.success(request, 'Password reset email has been sent')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Account doesnt exists')    
            return redirect('accounts:forgot_password')
        
class ResetPasswordView(View):
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
        
    def post(request):
         password= request.POST['password']
         confirm_password= request.POST['confirm_password']
         
         if password == confirm_password:
             uid= request.session.get('uid')
             user = Account.objects.get(pk=uid)
             user.set_password(password)
             user.save()
             messages.success(request, 'Password was resetted')
             return redirect('accounts:login')
         else:
            messages.error(request, 'Passwords dont match')    
            return redirect('accounts:forgot_password')
         

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "").lower()  # Normalize email to lowercase
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        
        if user:
            
            try:
               
                cart= Cart.objects.get(cart_session_id=Cart._get_cart_id(request)) 
                cart_item = CartItem.objects.filter(cart=cart)
                
                
                existing_user_cart_item= CartItem.objects.filter(user=user)     
                print(existing_user_cart_item)
                for item in cart_item:
                    product_variation=[]

                    if existing_user_cart_item.exists():
                        variation_found=False
                        product_variation.append(list(item.variation.all()))
                        print(product_variation)
                        for item_user in existing_user_cart_item:

                            existing_variations=[]    
                            existing_variations.append(list(item_user.variation.all()))
                            print(existing_variations[0])
                            print(product_variation == existing_variations)
                            if product_variation == existing_variations:
                                item_user.quantity +=item.quantity
                                item_user.save()
                                variation_found=True
                                break
                                
                                
                                
                        if not variation_found:
                            item.user = user
                            item.save()
                    else:

                        item.user = user
                        item.save()


            except:
                pass
            
            login(request, user)  # Create the session    
            refresh = RefreshToken.for_user(user)
            response = Response({
                'message': 'Login successful!',
            })
            # Set the access and refresh tokens in HTTP-only cookies
            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=False,
                secure=False,  # Set to True in production
                samesite='Lax',
                domain = os.environ.get('FRONTEND_DOMAIN')
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=False,
                secure=False,  # Set to True in production
                samesite='Lax',
                domain = os.environ.get('FRONTEND_DOMAIN')
            )
            return response
        else:
            return Response({"error": "Invalid credentials or account not verified"}, status=status.HTTP_401_UNAUTHORIZED)

        
class LogoutAPIView(APIView):
    
    def post(self, request):
        # Prepare the response
        logout(request)
        response = Response({"message": "Logout successful"})
        
        # Clear the cookies for access and refresh tokens
        response.delete_cookie('access_token' , domain = os.environ.get('FRONTEND_DOMAIN'))
        response.delete_cookie('refresh_token' , domain = os.environ.get('FRONTEND_DOMAIN'))
        
        # Attempt to blacklist the refresh token if provided
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                # Validate and blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
            return response
        except Exception as e:
            # Log the error for debugging
            print(f"Logout error: {str(e)}")
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Send verification email
            if os.environ.get('FRONTEND_DOMAIN') =="localhost":
                current_site ="localhost:3000"
            else:                
                current_site = os.environ.get('FRONTEND_DOMAIN')
            send_activation_email(user, current_site)
            return Response({"message": "Registration successful. Please verify your email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivateAccountAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:

            uid = urlsafe_base64_decode(uidb64).decode()
            print(uid)
            print(uidb64)
            print(token)
            user = Account._default_manager.get(pk=uid)
            #user = get_user_model().objects.get(pk=uid)
            print(user)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        print(account_activation_token.check_token(user, token))
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid or expired activation link."}, status=status.HTTP_400_BAD_REQUEST)



class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = get_user_model().objects.get(email=email)
            send_password_reset_email(user, request)
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            return Response({"error": "No account found with this email."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = ResetPasswordSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)



class ValidateTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # If the user is authenticated, return a success message
            return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
        except :
            logout(request)
            # Clear cookies if the token is invalid or expired
            response = Response({"message": "Token is invalid or expired"}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie('access_token' , domain = os.environ.get('FRONTEND_DOMAIN'))
            response.delete_cookie('refresh_token' , domain = os.environ.get('FRONTEND_DOMAIN'))

            # Optionally, blacklist the refresh token if it's provided and valid
            refresh_token = request.data.get("refresh")
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()  # Blacklist the refresh token
                except (InvalidToken, TokenError):
                    pass  # Handle any issues with the refresh token here if needed

            return response
