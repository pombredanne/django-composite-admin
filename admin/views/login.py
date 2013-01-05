from django import forms
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy

from base import Bootstrap


class LoginForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput(), initial='LoginForm', required=True)
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                message = ugettext_lazy("Please enter the correct username and password.")
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active:
                message = ugettext_lazy("Sorry, this account is desactivated.")
                raise forms.ValidationError(message)
        return self.cleaned_data


class LoginWidget(Bootstrap):

    template_name = 'adminnext/widgets/login.html'

    def __init__(self, parent=None, redirect_name=None, **kwargs):
        super(LoginWidget, self).__init__(parent, **kwargs)
        self.redirect_name = redirect_name

    def get_context_data(self, **kwargs):
        ctx = super(LoginWidget, self).get_context_data(**kwargs)
        ctx['form'] = LoginForm()
        return ctx

    def post(self, request, *args, **kwargs):
        if ('name' in request.POST and
            request.POST['name'] == 'LoginForm'):
            form = LoginForm(request.POST)
            if form.is_valid():
                login(request, form.user_cache)
                redirect_name = request.GET.get('next', self.redirect_name)
                return redirect(redirect_name)
            else:
                context = self.get_context_data(**kwargs)
                context['form'] = form
                return self.render_to_response(context)
        else:  # this is another form that was submitted
            return self.get(request, *args, **kwargs)


class Login(Bootstrap):

    composites = ((LoginWidget, 'adminnext:index'),)
