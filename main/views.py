from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect


# Home view
class HomeView(TemplateView):
    template_name = 'home.html'

# # Registration form view
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
# Custom login view with role-based redirect logic
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        next_url = request.GET.get('next')
        # Redirect regular users trying to access admin
        if next_url and next_url.startswith('/admin') and not request.user.is_staff:
            return HttpResponseRedirect(reverse('login'))

        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect(reverse_lazy('admin:index'))
            return redirect(reverse_lazy('user-dashboard'))
        
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return reverse('admin:index')
        return reverse('user-dashboard')

# Regular user dashboard (must be logged in)
@never_cache
@login_required
def user_dashboard_view(request):
    return render(request, 'dashboards/user_dashboard.html')

# Admin dashboard (must be logged in + is_staff)
# @user_passes_test(lambda u: u.is_staff)
# @login_required
# def admin_dashboard_view(request):
#     return render(request, 'dashboards/admin_dashboard.html')