from django.shortcuts import render
# from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserForm
# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

# class LogoutView(LogoutView):
#     next_page = '/login/'


class UpdateProfilePicture(TemplateView):
    model=CustomUser
    template_name='user_profile.html'
    form_class=CustomUserForm
    
    def post(self,request, *args, **kwargs):
        form=self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # user=request.user
            # user.image=request.FILES('image')
            form.save()
            return render(request, self.template_name)
        else:
            return self.form_invalid(form)
