from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Profile 
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm


def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"  # Ajoute ceci pour lier la vue au bon template

    def form_valid(self, form):
        # remember_me = form.cleaned_data.get('remember_me')
        response = super().form_valid(form)
        print(f"Utilisateur connecté : {self.request.user}") 
        print(f"Authentifié ? {self.request.user.is_authenticated}") 
        # Vérifier l'utilisateur authentifié
        return response
        # if not remember_me:
        #     self.request.session.set_expiry(0)
        #     self.request.session.modified = True

        # return super(CustomLoginView, self).form_valid(form)
     


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "Nous vous avons envoyé un e-mail contenant les instructions pour définir votre mot de passe, " \
                  "si un compte existe avec l'adresse e-mail que vous avez saisie. Vous devriez le recevoir sous peu. " \
                  "Si vous ne recevez pas cet e-mail, " \
                  "veuillez vérifier que vous avez bien entré l'adresse avec laquelle vous vous êtes inscrit, " \
                  "et consultez votre dossier spam."

    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')


@login_required
def profile(request):
    # Vérifier si l'utilisateur a un profil, sinon le créer
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('users:users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

def custom_logout(request):
    logout(request)
    return redirect('login')  