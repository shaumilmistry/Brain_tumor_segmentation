from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from Core.forms import BrainForm
from Core.models import Brain
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
import os
from .models import BrainImage
from .forms import BrainForm  
import os
import numpy as np
from PIL import Image
from django.conf import settings
from django.shortcuts import render
from .forms import BrainForm
from .models import BrainImage
from brats_final.predict import predict_segmentation  # your model import

def analyze_image(request):
    if request.method == 'POST':
        form = BrainForm(request.POST, request.FILES)
        if form.is_valid():
            image_obj = form.save()  # Save image to MEDIA_ROOT
            image_path = os.path.join(settings.MEDIA_ROOT, str(image_obj.image))

            # Predict segmentation mask
            output = predict_segmentation(image_path)  # assume this returns numpy array mask

            # Save mask to media/output
            output_image = Image.fromarray((output * 255).astype(np.uint8))
            output_dir = os.path.join(settings.MEDIA_ROOT, 'output')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f'output_{image_obj.id}.png')
            output_image.save(output_path)

            # Convert to URL
            mask_url = os.path.join(settings.MEDIA_URL, 'output', f'output_{image_obj.id}.png')

            return render(request, 'result.html', {
                'image': image_obj,
                'mask': mask_url
            })
    else:
        form = BrainForm()

    return render(request, 'upload.html', {'form': form})

@login_required
def Home(request):
    return render(request, 'index.html')

def RegisterView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")


        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email id already exists")

        if len(password) < 8:
            user_data_has_error = True
            messages.error(request, "Password must be atleast 8 characters")

        if password!=password2:
            user_data_has_error = True
            messages.error(request, "Please enter same password")
    
        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            messages.success(request, 'Account created. Login now')
            return redirect('login')

    return render(request, 'register.html')

def LoginView(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password")
            return redirect('login')

    return render(request, 'login.html')

def LogoutView(request):

    logout(request)

    return redirect('login')

def ForgotPassword(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body= f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        messages.error(request, 'Invalid email id')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            password_have_error = False

            if password != confirm_password:
                password_have_error = True
                messages.error(request, 'Passwords are not matching')

            if len(password) < 8:
                password_have_error = True
                messages.error(request, 'Password must be atleast 8 characters')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=5)

            if timezone.now() > expiration_time:
                password_have_error = True
                messages.error(request, 'Reset Password link has expired')

                reset_id.delete()

            if not password_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset is done. Please login')
                return redirect('login')
            
            else:
                return redirect('reset-password', reset_id=reset_id)

    except PasswordReset.DoesNotExist:

        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')    

    return render(request, 'reset_password.html')

def FormView(request):
    return render(request, 'form.html')

def upload_form(request):
    if request.method == "POST":
        print("POST request received!")  # Debugging step
        form = BrainForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid!")  # Debugging stepy
            form.save()
            print("Data saved!")  # Debugging step
            return redirect('home')  # Redirect to a success page
        else:
            print("Form is not valid!")
            print(form.errors)  # Print form validation errors
            return render(request, 'form.html', {'form': form})

    print("GET request received!")  # Debugging step
    return render(request, 'form.html', {'form': BrainForm()})

def upload_image(request):
    return render(request, 'upload.html')

# def show_result(request):
#     return render(request, 'result.html')