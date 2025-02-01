from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LoginMixn(LoginRequiredMixin):
    login_url = reverse_lazy('users:login')
    