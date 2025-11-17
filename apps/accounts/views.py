from django.shortcuts import render, get_object_or_404, redirect
import logging
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.http import url_has_allowed_host_and_scheme
from teknusa.utils import send_email, get_md5, get_current_site
from django.conf import settings

logger = logging.getLogger(__name__)


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/registration_form.html'

    def form_valid(self, form):
        user = form.save(False)
        user.is_active = False
        user.source = 'Register'
        user.save(True)
        site = get_current_site().domain
        sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))

        if settings.DEBUG:
            site = '127.0.0.1:8000'
        path = reverse('account:result')
        url = f"http://{site}{path}?type=validation&id={user.id}&sign={sign}"

        content = f"""
            <p>Please click on the link below to verify your email</p>
            <a href="{url}" rel="bookmark">{url}</a>
            Thank you again!
            <br />
            If the link above does not open, copy it to your browser.
            {url}
        """
        send_email(emailto=[user.email], title='Verify your email', content=content)

        success_url = '/' + f'?type=register&id={user.id}'
        return HttpResponseRedirect(success_url)


class LogoutView(RedirectView):
    url = '/'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        from teknusa.utils import cache
        cache.clear()
        logout(request)
        return super().get(request, *args, **kwargs)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('dashboard')
    redirect_field_name = 'next'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)
        if form.is_valid():
            from teknusa.utils import cache
            if cache:
                cache.clear()
            login(self.request, form.get_user())
            return super().form_valid(form)
        else:
            return self.render_to_response({'form': form})

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name, self.success_url)
        if not url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts={self.request.get_host()}):
            redirect_to = self.success_url
        return redirect_to


def account_result(request):
    type_ = request.GET.get('type')
    user_id = request.GET.get('id')
    user = get_object_or_404(get_user_model(), id=user_id)

    if user.is_active:
        return redirect('/')

    if type_ in ['register', 'validation']:
        if type_ == 'register':
            content = f'Congratulations! A verification email has been sent to {user.email}.'
            title = 'Registration Successful'
        else:
            c_sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))
            sign = request.GET.get('sign')
            if sign != c_sign:
                return HttpResponseForbidden()
            user.is_active = True
            user.save()
            content = 'Congratulations! Your email has been verified.'
            title = 'Validation Successful'

        return render(request, 'account/result.html', {'title': title, 'content': content})
    return redirect('/')
