from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView

from src.forms import RegisterForm


@login_required
def keywords_view(request):
    return render(request, 'src/keywords.html')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("src:keywords")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

