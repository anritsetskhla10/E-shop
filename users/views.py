from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from shop.models import Product
from .forms import UserRegisterForm


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'რეგისტრაცია წარმატებით დასრულდა. გთხოვთ გაიაროთ ავტორიზაცია.')
        return response


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f'მოგესალმებით, {form.get_user().username}!')
        return super().form_valid(form)


def user_logout_view(request):
    logout(request)
    messages.info(request, 'თქვენ გამოხვედით სისტემიდან.')
    return redirect('shop:home')


@login_required
def profile_view(request):
    user_products = Product.objects.filter(user=request.user).order_by('-id')
    context = {
        'user': request.user,
        'user_products': user_products,
        'total_products': user_products.count(),
    }
    return render(request, 'users/profile.html', context)